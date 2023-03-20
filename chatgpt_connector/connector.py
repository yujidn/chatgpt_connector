import os
import typing

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_text(text: str, model="gpt-3.5-turbo") -> openai.openai_object.OpenAIObject:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
        ],
    )

    return response


def send_messages(
    messages: typing.List[dict], *, model="gpt-3.5-turbo", max_tokens=1024
) -> openai.openai_object.OpenAIObject:
    """
    {"role": <role>, "content": <text>},
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    return response


def response_to_text(response: openai.openai_object.OpenAIObject) -> str:
    usd_to_jpg = 140
    token_cost = response["usage"]["total_tokens"]
    usd_cost = response["usage"]["total_tokens"] / 1000 * 0.002
    jpy_cost = usd_cost * usd_to_jpg

    text = response["choices"][0]["message"]["content"] + "\n"
    # cost_text = f"ちなみに、このテキストを作るのに{token_cost}トークン使用し、{jpy_cost}円かかりました。({usd_to_jpg}yen/usd換算)" + "\n"
    # text += cost_text
    print(f"token:{token_cost} jpy:{jpy_cost}")

    return text
