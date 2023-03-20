# python_repository_template

## 環境構築

```cmd
python -m venv .venv
.venv/bin/activate # linux
.venv/Scripts/activate # windows
poetry install
```

## 動かし方

### [共通] OpenAI API Token

OpenAIにログインできる状態で、[このあたり](https://platform.openai.com/account/api-keys)から発行できる。
以下のように環境変数に登録する。

```cmd
export OPENAI_API_KEY=****
```

### slack bot

slackのアプリ作成は[このあたり](https://slack.dev/bolt-js/ja-jp/tutorial/getting-started)からにある。
ただし、permission設定が緩いので、mentionだけ受け取れるようにしたほうが良い。

詳細はTBD

### slack bot (aws lambda)

TBD

### discord bot

[このあたり](https://discordpy.readthedocs.io/ja/latest/discord.html)を参考にbotを導入し、tokenを以下のように環境変数に登録する。

```cmd
export DISCORD_TOKEN=****
```

```cmd
python discord_bot.py
```
