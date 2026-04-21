# AWS SDK for Python (boto3) サンプルコード

AWS SDK for Python (boto3) を使用した各サービスの操作サンプル集です。

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- 利用するリージョンは us-west-2 (オレゴン)

---

## セットアップ

### 1. リポジトリをクローンする

```bash
git clone https://github.com/tetsuo-nobe/aws-python-basic.git
```

### 2. boto3 をインストールする

```bash
pip3 install boto3
```

---

## フォルダ構成

```
aws_sdk/
├── s3/          ... Amazon S3 の操作サンプル
├── bedrock/     ... Amazon Bedrock の操作サンプル
└── README.md
```

---

## s3 - Amazon S3 操作サンプル

S3 Client API を使用したバケット・オブジェクト操作のサンプルです。ファイル名の番号順に実行することで、バケットの作成からオブジェクト操作、削除までの一連の流れを体験できます。

### 事前準備

`mybucket.py` の `bucket_name` を自分のバケット名に変更してください。バケット名はグローバルで一意である必要があります。

### ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `mybucket.py` | バケット名を定義する共通設定ファイル（各サンプルから import される） |
| `client01-create-bucket.py` | バケットを作成する |
| `client02-put-object.py` | `put_object` でオブジェクトをバケットに格納する |
| `client03-upload-file.py` | `upload_file` でファイルをバケットにアップロードする |
| `client04-get-object.py` | `get_object` でオブジェクトを取得しローカルに保存する |
| `client05-download-file.py` | `download_file` でオブジェクトをダウンロードする |
| `client08-delete-object.py` | オブジェクトを削除する |
| `client11-presigned_url.py` | 署名付き URL を生成する |
| `client12-delete-bucket.py` | バケット内の全オブジェクトを削除した後、バケットを削除する |
| `cat.jpg` | サンプル用の画像ファイル（`client02`、`client04`、`client11` で使用） |
| `Eiffel.jpg` | サンプル用の画像ファイル（`client03`、`client05`、`client08` で使用） |

### 実行例

```bash
cd aws_sdk/s3
python3 client01-create-bucket.py
```

---

## bedrock - Amazon Bedrock 操作サンプル

Amazon Bedrock の Converse API を使用して基盤モデル（Amazon Nova Lite）と会話するサンプルです。

### 追加の前提条件

- Amazon Bedrock で `us.amazon.nova-lite-v1:0` モデルが使用できること

### ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `converse_api.py` | Converse API で複数ターンの会話を行うサンプル。日本の四季の行事について質問し、追加で秋の行事を深掘りする |
| `converse_stream_api.py` | Converse Stream API でレスポンスをリアルタイムに逐次表示するサンプル。日本各地のご当地ラーメンについて質問する |

### 実行例

```bash
cd aws_sdk/bedrock
python3 converse_api.py
python3 converse_stream_api.py
```

---

## プログラミング課題: Bedrock × S3 連携

ここまでのサンプルコードで学んだ内容を活用して、以下の課題に挑戦してください。`bedrock` フォルダに `challenge.py` を作成してコードを記述します。

### 課題内容

ユーザーが入力したプロンプトを Amazon Bedrock の基盤モデルに送信し、返ってきたレスポンスを Amazon S3 バケットに保存するプログラムを作成してください。

#### 処理の流れ

1. プロンプト（質問文）を文字列の変数として定義する
2. Amazon Bedrock の Converse API を使用して基盤モデル（`us.amazon.nova-lite-v1:0`）にリクエストを送信する
3. モデルから返ってきたレスポンス（テキスト）を取得する
4. プロンプトとレスポンスを合わせたテキストを S3 バケットにオブジェクトとして格納する
5. 格納が完了したら、保存先のバケット名とオブジェクトキーを表示する

#### 前提条件

- S3 バケットは `s3/client01-create-bucket.py` で作成済みのものを使用します（新たに作成する必要はありません）
- バケット名は `s3/mybucket.py` の `bucket_name` を import して使用してください

#### 要件

| 項目 | 内容 |
|------|------|
| モデル ID | `us.amazon.nova-lite-v1:0` |
| API | Bedrock Runtime の Converse API（`converse` メソッド） |
| システムプロンプト | 自由に設定してください（例：「あなたは親切なアシスタントです。」） |
| プロンプト定義 | 文字列の変数として定義する（例：`prompt = "日本で一番高い山はなんですか？"`） |
| S3 格納内容 | プロンプトとレスポンスの両方を含むテキスト |
| S3 オブジェクトキー | 任意（例：`bedrock-response.txt`、タイムスタンプを含めると重複を避けられます） |
| エラー処理 | `try`/`except` で適切にエラーハンドリングを行う |

### 期待される実行結果の例

```
プロンプト: 日本で一番高い山はなんですか？
Bedrock にリクエストを送信中...

--- Bedrock のレスポンス ---
日本で一番高い山は富士山です。標高は3,776メートルで...
--------------------------

S3 に保存しました。
  バケット: notes-bucket-xxxxxxxx
  キー: bedrock-response-20250417-123456.txt
```

### ヒント

- `converse_api.py` の Converse API の呼び出し方を参考にしてください
- プロンプトは以下のように変数として定義します
  ```python
  prompt = "日本で一番高い山はなんですか？"
  ```
- `s3/client02-put-object.py` の `put_object` によるオブジェクト格納を参考にしてください
- `s3/mybucket.py` からバケット名を import する際は、`sys.path` にパスを追加する必要があります
  ```python
  import sys
  sys.path.append('../s3')
  from mybucket import bucket_name as bucket
  ```
- S3 に格納する際、`Body` にはバイト列を渡す必要があります。文字列は `.encode('utf-8')` でバイト列に変換してください
  ```python
  text = "こんにちは"
  body = text.encode('utf-8')  # 文字列をバイト列に変換
  ```
- オブジェクトキーにタイムスタンプを含める場合は、`standard_library.py` で学んだ `time` モジュールや `datetime` モジュールが使えます
  ```python
  from datetime import datetime
  timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
  key = f'bedrock-response-{timestamp}.txt'
  ```

### 実行方法

```bash
cd aws_sdk/bedrock
python3 challenge.py
```
