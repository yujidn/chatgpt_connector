import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from chatgpt_connector import connector

app = App(token=os.getenv("SLACK_BOT_TOKEN"))


# スレッドを作成する関数
def reply_thread(channel_id, thread_ts, text):
    app.client.chat_postMessage(channel=channel_id, text=text, thread_ts=thread_ts)


@app.event("app_mention")
def handle_mention(event, say):
    import json

    user_id = event["user"]
    channel_id = event["channel"]

    # スレッドのタイムスタンプを取得する
    thread_ts = event["thread_ts"] if "thread_ts" in event else event["ts"]

    response = app.client.conversations_replies(channel=channel_id, ts=thread_ts)
    messages = response["messages"]

    # 指定されたユーザによるメッセージを取得する
    user_messages = []
    for message in messages:
        print(json.dumps(message, indent=2))
        if message.get("user") == user_id:
            user_messages.append(message)

    # メッセージをまとめる
    thread_message = ""
    for user_message in user_messages:
        # メッセージの先頭にあるuser_idをskipする
        text = user_message["text"][len(user_id) + 5 :]
        thread_message += "{}\n".format(text)

    print(thread_message)

    try:
        response = connector.send_text(thread_message)
        response_text = connector.response_to_text(response)
        print(response_text)
        # スレッドで返信する
        response_text = f"<@{user_id}> {response_text}"
        reply_thread(channel_id, thread_ts, response_text)
    except Exception as e:
        say(f"なんかエラーだって {e}")


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
