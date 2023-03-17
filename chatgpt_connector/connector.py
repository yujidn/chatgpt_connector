import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_message(text: str, model="gpt-3.5-turbo") -> openai.openai_object.OpenAIObject:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "質問が来た場合は質問への回答をしてください。チャットが来た場合はチャットへの返答をしてください。回答はmarkdown形式で記載してください。",
            },
            {"role": "user", "content": text},
        ],
    )

    return response


def response_to_text(response: openai.openai_object.OpenAIObject) -> str:
    usd_to_jpg = 140
    token_cost = response["usage"]["total_tokens"]
    usd_cost = response["usage"]["total_tokens"] / 1000 * 0.002
    jpy_cost = usd_cost * usd_to_jpg

    text = response["choices"][0]["message"]["content"] + "\n"
    text += f"ちなみに、このテキストを作るのに{token_cost}トークン使用し、{jpy_cost}円かかりました。({usd_to_jpg}yen/usd換算)" + "\n"

    return text
