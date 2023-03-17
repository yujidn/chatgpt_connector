import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from chatgpt_connector import connector

app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.event("app_mention")
def handle_mention(event, say):
    text = event["text"]
    user_id = event["user"]
    print(f"get_message:{text}")
    try:
        response = connector.send_message(text)
        response_text = connector.response_to_text(response)
        print(response_text)
        say(f"<@{user_id}> {response_text}")
    except Exception as e:
        say(f"なんかエラーだって {e}")


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
