## コード開発用ディレクトリ

```
npm install -g serverless
sls
```

対話でセットアップ

```
? What do you want to make? AWS - Python - Starter
? What do you want to call this project? chatgpt-lambda

✔ Project successfully created in chatgpt-lambda folder

? Do you want to login/register to Serverless Dashboard? No
```

セットアップ後に `handler.py` と `serverless.yml` を書き換えてdeploy.

```
cd chatgpt-lambda
sls plugin install -n serverless-python-requirements
serverless deploy --aws-profile {your aws confidential profile name}
```


## lambdaにレイヤー追加

$ mkdir python
$ pip install openai -t ./python
$ zip -r9 layer.zip python
zipをlambdaのレイヤーに新規追加


## aws consoleでやること

* デプロイしたlambda関数上で、関数のlayerに上で追加したopenaiを追加する
* 同時実行の予約数を1にする
