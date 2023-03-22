import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from chatgpt_connector import connector

app = App(token=os.getenv("SLACK_BOT_TOKEN"))
bot_user_id = app.client.auth_test()["user_id"]


def remove_mention(message: str) -> str:
    m = re.match("<@.*>", message)
    if m is not None:
        return message[m.span()[1] :]
    return message


# スレッドを作成する関数
def reply_thread(channel_id, thread_ts, text):
    app.client.chat_postMessage(channel=channel_id, text=text, thread_ts=thread_ts)


@app.event("app_mention")
def handle_mention(event, say):
    user_id = event["user"]
    channel_id = event["channel"]

    # スレッドのタイムスタンプを取得する
    thread_ts = event["thread_ts"] if "thread_ts" in event else event["ts"]

    response = app.client.conversations_replies(channel=channel_id, ts=thread_ts)
    messages = response["messages"]

    # 指定されたユーザによるメッセージを取得する
    message_prompt = []
    for message in messages:
        if message.get("user") != bot_user_id:
            message_prompt.append({"role": "user", "content": remove_mention(message["text"])})
        else:
            message_prompt.append({"role": "assistant", "content": remove_mention(message["text"])})

    system_prompt = [
        {
            "role": "system",
            "content": "最新のメッセージ以外は会話の履歴です。roleがuserのものはユーザーが発したもので、roleがassistantのものは、chatgptからの返答になっています。会話履歴を踏まえたうえで、最新のメッセージに回答してください。",
        }
    ]

    message_list = system_prompt + message_prompt

    try:
        response = connector.send_messages(message_list)
        response_text = connector.response_to_text(response)
        # スレッドで返信する
        response_text = f"<@{user_id}> {response_text}"
        reply_thread(channel_id, thread_ts, response_text)
    except Exception as e:
        say(f"なんかエラーだって {e}")


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
