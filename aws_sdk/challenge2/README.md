# プログラミング課題 2: DynamoDB × S3 連携（スコアレポート生成）

DynamoDB テーブルからスコアデータを検索し、テキストレポートを作成して S3 バケットに保存し、署名付き URL を生成するプログラムを作成する課題です。

## 課題内容

特定ユーザーのゲームスコアデータを DynamoDB から取得し、整形したテキストレポートを S3 に保存して、署名付き URL で共有できるようにしてください。`challenge.py` にコードを記述します。

### 処理の流れ

1. DynamoDB の `query` で特定ユーザー（`userId`）の値が 3 のスコアデータを取得する
2. 取得結果を整形してテキストレポートを作成する
3. レポートを S3 バケットにオブジェクト(.txt ファイル）として保存する
4. 保存したオブジェクトの署名付き URL (有効期間 60秒）を生成して表示する

---

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- 利用するリージョンは us-west-2 (オレゴン)

---

## 事前準備

### 1. 設定ファイルを編集する

`myconfig.py` の `bucket_name` を自分のユニークなバケット名に変更してください。

```python
# myconfig.py
bucket_name = "challenge2-report-xxxxxxxx"  # ← 自分のユニークなバケット名に変更
table_name = "score"
```

### 2. リソースを作成する

`1_create_resources.py` を実行して、DynamoDB テーブルと S3 バケットを作成します。

```bash
cd aws_sdk/challenge2
python3 1_create_resources.py
```

以下のリソースが作成されます。

| リソース | 名前 | 説明 |
|---------|------|------|
| DynamoDB テーブル | `score` | パーティションキー: `userId`（数値）、ソートキー: `gameId`（文字列） |
| DynamoDB データ | 10 件 | `score_data.json` からロードされるサンプルデータ |
| S3 バケット | `myconfig.py` で指定した名前 | レポートの保存先 |

---

## ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `myconfig.py` | バケット名・テーブル名を定義する共通設定ファイル |
| `score_data.json` | DynamoDB にロードするサンプルデータ |
| `1_create_resources.py` | 事前準備スクリプト（DynamoDB テーブル作成・データロード・S3 バケット作成） |
| `challenge.py` | 課題のテンプレート（ここにコードを記述する） |
| `challenge_answer.py` | 課題の解答例 |
| `9_delete_resources.py` | クリーンアップスクリプト（S3 バケット・DynamoDB テーブルの削除） |

---

## 要件

| 項目 | 内容 |
|------|------|
| 検索対象 | `userId` を指定して DynamoDB テーブルを検索する |
| DynamoDB API | Client API の `query` メソッド |
| レポート内容 | ユーザー ID、各ゲームのスコアと残機（life）を含むテキスト |
| S3 API | Client API の `put_object` メソッド |
| S3 オブジェクトキー | 任意（タイムスタンプを含めると重複を避けられる） |
| 署名付き URL | `generate_presigned_url` で生成し、有効期限を設定する |
| エラー処理 | `try`/`except` で適切にエラーハンドリングを行う |

---

## 期待される実行結果の例

```
DynamoDB テーブル 'score' から userId=3 のデータを検索中...
4 件のアイテムを取得しました。

--- 生成されたレポート ---
========================================
  スコアレポート (userId: 3)
  作成日時: 2025-04-21 14:30:00
========================================

  ゲーム ID : G001
  スコア   : 3100
  ライフ   : 3
----------------------------------------
  ゲーム ID : G002
  スコア   : 3200
  ライフ   : 2
----------------------------------------
  ゲーム ID : G003
  スコア   : 3300
  ライフ   : 1
----------------------------------------
  ゲーム ID : G004
  スコア   : 3400
  ライフ   : 2
----------------------------------------

  合計ゲーム数: 4
========================================
--------------------------

S3 に保存しました。
  バケット: challenge2-report-xxxxxxxx
  キー: score-report-user3-20250421-143000.txt

署名付き URL（有効期限: 60 秒）:
  https://challenge2-report-xxxxxxxx.s3.amazonaws.com/score-report-user3-...
```

---

## ヒント

- `dynamodb/query.py` の `query` によるパーティションキー検索を参考にしてください
  ```python
  response = ddb_client.query(
      TableName=table_name,
      KeyConditionExpression="userId = :userId",
      ExpressionAttributeValues={
          ":userId": {"N": str(target_user_id)}
      },
  )
  items = response["Items"]
  ```

- DynamoDB の `query` の結果は型付きの辞書（例: `{"N": "3100"}`）で返されます。`TypeDeserializer` を使うと通常の Python の値に変換できます
  ```python
  from boto3.dynamodb.types import TypeDeserializer
  deserializer = TypeDeserializer()
  data = {key: deserializer.deserialize(value) for key, value in item.items()}
  ```

- `s3/client02-put-object.py` の `put_object` によるオブジェクト格納を参考にしてください。テキストデータは `.encode("utf-8")` でバイト列に変換して `Body` に渡します
  ```python
  s3_client.put_object(
      Body=report_text.encode("utf-8"),
      Bucket=bucket_name,
      Key=key,
  )
  ```

- `s3/client11-presigned_url.py` の `generate_presigned_url` を参考にしてください
  ```python
  url = s3_client.generate_presigned_url(
      ClientMethod="get_object",
      Params={"Bucket": bucket_name, "Key": key},
      ExpiresIn=60,
      HttpMethod="GET",
  )
  ```

- オブジェクトキーにタイムスタンプを含める場合は `datetime` モジュールが使えます
  ```python
  from datetime import datetime
  timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
  key = f"score-report-user{target_user_id}-{timestamp}.txt"
  ```

---

## 実行方法

```bash
cd aws_sdk/challenge2
python3 challenge.py
```

---

## クリーンアップ

課題が終了したら、`9_delete_resources.py` を実行してリソースを削除します。

```bash
python3 9_delete_resources.py
```

以下のリソースが削除されます。
- S3 バケット内の全オブジェクトとバケット本体
- DynamoDB テーブル
