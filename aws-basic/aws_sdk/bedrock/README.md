# Amazon Bedrock 操作サンプル

Amazon Bedrock の Converse API を使用して基盤モデル（Amazon Nova Lite）と会話するサンプルです。

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- Amazon Bedrock で `us.amazon.nova-lite-v1:0` モデルが使用できること
- 利用するリージョンは us-west-2 (オレゴン)

---

## ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `converse_api.py` | Converse API で複数ターンの会話を行うサンプル。日本の四季の行事について質問し、追加で秋の行事を深掘りする |
| `converse_stream_api.py` | Converse Stream API でレスポンスをリアルタイムに逐次表示するサンプル。日本各地のご当地ラーメンについて質問する |

---

## 実行方法

```bash
cd aws_sdk/bedrock

# Converse API（複数ターンの会話）
python3 converse_api.py

# Converse Stream API（ストリーミング表示）
python3 converse_stream_api.py
```

---

## サンプルコードの解説

### converse_api.py — 複数ターンの会話

Converse API を使って、会話履歴を保持しながら複数回のリクエストを送信するサンプルです。

- 1 回目のリクエスト: 日本の四季の行事について質問する
- レスポンスを会話履歴（`messages` リスト）に追加する
- 2 回目のリクエスト: 1 回目の回答を踏まえて秋の行事を深掘りする

> 会話履歴をリクエストに含めることで、モデルが前の文脈を踏まえた回答を生成します。

### converse_stream_api.py — ストリーミング表示

Converse API のストリーミング版（`converse_stream`）を使って、レスポンスをリアルタイムに逐次表示するサンプルです。

- 通常の `converse` はレスポンス全体が返るまで待つ
- `converse_stream` はテキストが生成されるたびに逐次受信・表示できる
- トークン使用量やレイテンシなどのメタデータも取得できる

---

## 学習ポイント

| テーマ | 内容 |
|--------|------|
| Converse API | モデルに対してメッセージを送信し、レスポンスを受け取る統一的な API |
| 複数ターンの会話 | 会話履歴を `messages` リストに蓄積して文脈を維持する |
| ストリーミング | `converse_stream` でレスポンスをリアルタイムに逐次表示する |
| システムプロンプト | モデルの役割や回答スタイルを定義する |
| 推論パラメータ | `temperature` などでモデルの出力を制御する |
