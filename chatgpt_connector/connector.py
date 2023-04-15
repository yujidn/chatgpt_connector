import json
import os
import typing

import requests

from .logger import get_logger

url = "https://api.openai.com/v1/chat/completions"
api_key = os.getenv("OPENAI_API_KEY")
TIMEOUT = 5
logger = get_logger()


def send_messages(messages: typing.List[dict], *, model="gpt-3.5-turbo", max_tokens=1024) -> dict:
    """
    list型のメッセージをopen ai apiに投げ込む.
    messagesは
    [
        {
            "role": "system" or "user" or "assistant",
            "content": "text"
        },
        {
            ...
        }, ...
    ]
    のような並び.
    "role"は、systemで恒久的なルールを、userでopenaiに聞いたtextを、assistantでoepnaiから返答をいれることで、会話の履歴を再現できる。

    Args:
        messages (typing.List[dict]): _description_
        model (str, optional): _description_. Defaults to "gpt-3.5-turbo".
        max_tokens (int, optional): _description_. Defaults to 1024.

    Returns:
        example
        {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "choices": [{
                "index": 0,
                "message": {
                "role": "assistant",
                "content": "\n\nHello there, how may I assist you today?",
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
            }
        }

    """

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    logger.debug(json.dumps(messages))

    response = requests.post(url, headers=headers, json=messages, timeout=(TIMEOUT, TIMEOUT))

    logger.debug(f"status_code:{response.status_code}")

    if response.status_code == 200:
        result = response.json()
        logger.debug(json.dumps(result))
        return result

    else:
        # https://platform.openai.com/docs/guides/error-codes
        raise Exception(
            f"request error_code:{response.status_code}\n detail -> https://platform.openai.com/docs/guides/error-codes"
        )


def response_to_text(response: dict) -> str:
    usd_to_jpg = 140
    usd_cost = response["usage"]["total_tokens"] / 1000 * 0.002
    jpy_cost = usd_cost * usd_to_jpg

    text = response["choices"][0]["message"]["content"] + "\n"
    logger.info(json.dumps({**response["usage"], "jpy": jpy_cost}))

    return text
