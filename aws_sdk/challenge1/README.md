# プログラミング課題 1: Bedrock × S3 連携

ここまでのサンプルコードで学んだ内容を活用して、以下の課題に挑戦してください。`challenge.py` にコードを記述します。

## 課題内容

プロンプトを Amazon Bedrock の基盤モデルに送信し、返ってきたレスポンスを Amazon S3 バケットに保存するプログラムを作成してください。

### 処理の流れ

1. プロンプト（質問文）を文字列の変数として定義する
2. Bedrock の Converse API で基盤モデル（`us.amazon.nova-lite-v1:0`）にリクエストを送信する
3. モデルから返ってきたレスポンス（テキスト）を取得する
4. プロンプトとレスポンスを合わせたテキストを S3 バケットにオブジェクトとして格納する
5. 格納が完了したら、保存先のバケット名とオブジェクトキーを表示する

---

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- Amazon Bedrock で `us.amazon.nova-lite-v1:0` モデルが使用できること
- **S3 バケットが `s3/client01-create-bucket.py` で作成済みであること**
    - すでに削除している場合は、再度実行してバケットを作成しておいてください。
    - ```
      python3 ../s3/client01-create-bucket.py
      ```

---

## ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `challenge.py` | 課題のテンプレート（ここにコードを記述する） |
| `challenge_answer.py` | 課題の解答例 |

---

## 要件

| 項目 | 内容 |
|------|------|
| モデル ID | `us.amazon.nova-lite-v1:0` |
| API | Bedrock Runtime の Converse API（`converse` メソッド） |
| システムプロンプト | 自由に設定（例：「あなたは親切なアシスタントです。」） |
| プロンプト定義 | 文字列の変数として定義する（例：`prompt = "日本で一番高い山はなんですか？"`） |
| S3 格納内容 | プロンプトとレスポンスの両方を含むテキスト |
| S3 オブジェクトキー | 任意（タイムスタンプを含めると重複を避けられる） |
| エラー処理 | `try`/`except` で適切にエラーハンドリングを行う |

---

## 期待される実行結果の例

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

---

## ヒント

- `bedrock/converse_api.py` の Converse API の呼び出し方を参考にしてください
- プロンプトは以下のように変数として定義します
  ```python
  prompt = "日本で一番高い山はなんですか？"
  ```
- `s3/client02-put-object.py` の `put_object` によるオブジェクト格納を参考にしてください
- `s3/mybucket.py` からバケット名を import する際は `sys.path` にパスを追加してください
  ```python
  import sys
  sys.path.append('../s3')
  from mybucket import bucket_name as bucket
  ```
- S3 の `Body` にはバイト列を渡す必要があります（`.encode('utf-8')` で変換）
  ```python
  text = "こんにちは"
  body = text.encode('utf-8')  # 文字列をバイト列に変換
  ```
- オブジェクトキーにタイムスタンプを含める場合は `datetime` モジュールが使えます
  ```python
  from datetime import datetime
  timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
  key = f'bedrock-response-{timestamp}.txt'
  ```

---

## 実行方法

```bash
cd aws_sdk/challenge1
python3 challenge.py
```

---

## 課題修了時にバケットを削除

- 課題修了時は下記を実行し、バケット内のオブジェクトとバケットを削除しておいてください。
    - ```
      python3 ../s3/client12-delete-bucket.py
      ```

