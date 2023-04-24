import logging
import os
import re

import discord
from discord.ext import commands

from chatgpt_connector import connector, logger

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)


def remove_mention(message: str) -> str:
    m = re.match("<.*>", message)
    if m is not None:
        return message[m.span()[1] :]
    return message


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.event
async def on_message(message: discord.message.Message):
    if bot.user.mentioned_in(message):
        # メンションされた場合の処理
        await message.add_reaction("👍")
        history_prompt = []
        system_prompt = [
            {
                "role": "system",
                "content": "最新のメッセージ以外は会話の履歴です。roleがuserのものはユーザーが発したもので、roleがassistantのものは、chatgptからの返答になっています。会話履歴を踏まえたうえで、最新のメッセージに回答してください。",
            }
        ]
        history_prompt.append({"role": "user", "content": remove_mention(message.content)})
        async for msg in message.channel.history(limit=2, before=message):
            if msg.content:
                # bot 以外のユーザーのメッセージのみリストに追加する
                content = remove_mention(msg.content)
                if "chatgpt" in msg.author.name:
                    history_prompt.append({"role": "assistant", "content": content})
                else:
                    history_prompt.append({"role": "user", "content": content})

        history_prompt.reverse()

        message_list = system_prompt + history_prompt
        # import json
        # print(json.dumps(message_list, indent=2, ensure_ascii=False))

        try:
            response = connector.send_messages(message_list)
            res_text = connector.response_to_text(response)
            # print(res_text)
            await message.channel.send(f"{message.author.mention} {res_text}")
        except Exception as e:
            await message.channel.send(f"{message.author.mention} 何かエラーが起きました。 {e}")


bot.run(os.getenv("DISCORD_TOKEN"), log_handler=logger.get_logger().handlers[0], log_level=logging.DEBUG)
