# プログラミング課題 3: DynamoDB GSI × S3 連携（ゲームランキング生成＆条件付きボーナス付与）

DynamoDB の GSI（グローバルセカンダリインデックス）を使ってゲームのスコアランキングを取得し、1位プレイヤーに条件付きでボーナスライフを付与した後、ランキングレポートを S3 に保存して署名付き URL で共有するプログラムを作成する課題です。

## 課題内容

指定したゲームのスコアランキングを GSI から降順で取得し、1位プレイヤーへの条件付き更新を行い、結果をレポートとして S3 に保存してください。`challenge.py` にコードを記述します。

### 処理の流れ

1. GSI (`game_index`) に対して `query` を実行し、指定ゲームのスコアを**降順**で取得する
2. ランキング 1 位のプレイヤーに対し、`update_item` で条件付きボーナスライフを付与する（条件: `life` が 3 未満の場合のみ +1）
3. ランキング結果をテキストレポートとして整形する
4. レポートを S3 バケットに `put_object` で保存する
5. 保存したオブジェクトの署名付き URL（有効期限 60 秒）を生成して表示する

---

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- 利用するリージョンは ap-northeast-1 (東京)

---

## 事前準備

### 1. 設定ファイルを編集する

`myconfig.py` の `bucket_name` を自分のユニークなバケット名に変更してください。

```python
# myconfig.py
bucket_name = "challenge3-ranking-xxxxxxxx"  # ← 自分のユニークなバケット名に変更
table_name = "score"
index_name = "game_index"
```

### 2. リソースを作成する

`1_create_resources.py` を実行して、DynamoDB テーブル・GSI・S3 バケットを作成します。

```bash
cd aws_sdk/challenge3
python3 1_create_resources.py
```

> **注意**: GSI の作成には数分かかります。スクリプトは作成完了まで待機します。

以下のリソースが作成されます。

| リソース | 名前 | 説明 |
|---------|------|------|
| DynamoDB テーブル | `score` | パーティションキー: `userId`（数値）、ソートキー: `gameId`（文字列） |
| DynamoDB GSI | `game_index` | パーティションキー: `gameId`（文字列）、ソートキー: `score`（数値） |
| DynamoDB データ | 10 件 | `score_data.json` からロードされるサンプルデータ |
| S3 バケット | `myconfig.py` で指定した名前 | ランキングレポートの保存先 |

---

## ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `myconfig.py` | バケット名・テーブル名・インデックス名を定義する共通設定ファイル |
| `score_data.json` | DynamoDB にロードするサンプルデータ |
| `1_create_resources.py` | 事前準備スクリプト（DynamoDB テーブル・GSI 作成・データロード・S3 バケット作成） |
| `challenge.py` | 課題のテンプレート（ここにコードを記述する） |
| `9_delete_resources.py` | クリーンアップスクリプト（S3 バケット・DynamoDB テーブルの削除） |

---

## 要件

| 項目 | 内容 |
|------|------|
| ランキング取得対象 | `gameId` を指定して GSI をクエリする |
| DynamoDB クエリ API | Client API の `query` メソッド（`IndexName` を指定） |
| ソート順 | `ScanIndexForward=False` でスコア降順（ランキング順） |
| 条件付き更新 | `update_item` で `ConditionExpression` を使用し、`life < 3` の場合のみ `life` を +1 する |
| 条件不一致時の処理 | `ConditionalCheckFailedException` をキャッチして適切にメッセージを表示する |
| レポート内容 | ゲーム ID、各プレイヤーの順位・スコア・ライフを含むテキスト |
| S3 API | Client API の `put_object` メソッド |
| S3 オブジェクトキー | 任意（タイムスタンプを含めると重複を避けられる） |
| 署名付き URL | `generate_presigned_url` で生成し、有効期限 60 秒を設定する |
| エラー処理 | `try`/`except` で適切にエラーハンドリングを行う |

---

## 期待される実行結果の例

```
ゲーム 'G001' のランキングを取得中...（スコア降順）
3 件のアイテムを取得しました。

--- G001 ランキング ---
  1位: userId=3, スコア=3100, ライフ=3
  2位: userId=2, スコア=1100, ライフ=2
  3位: userId=1, スコア=1000, ライフ=1
------------------------------

1位のプレイヤー (userId=3) にボーナスライフを付与中...
  条件: ライフが 3 未満の場合のみ +1
  結果: 条件を満たさないため更新をスキップしました。（ライフが既に 3 以上）

--- 生成されたレポート ---
========================================
  ゲームランキングレポート (G001)
  作成日時: 2025-06-04 12:00:00
========================================

  1位
    ユーザー ID : 3
    スコア     : 3100
    ライフ     : 3
----------------------------------------
  2位
    ユーザー ID : 2
    スコア     : 1100
    ライフ     : 2
----------------------------------------
  3位
    ユーザー ID : 1
    スコア     : 1000
    ライフ     : 1
----------------------------------------

  参加プレイヤー数: 3
========================================
--------------------------

S3 に保存しました。
  バケット: challenge3-ranking-xxxxxxxx
  キー: ranking-G001-20250604-120000.txt

署名付き URL（有効期限: 60 秒）:
  https://challenge3-ranking-xxxxxxxx.s3.amazonaws.com/ranking-G001-...
```

> **補足**: サンプルデータでは userId=3 の G001 のライフが 3 のため、条件（life < 3）を満たさず更新はスキップされます。別のゲーム ID（例: `G002`）で実行すると、1位プレイヤーのライフが 3 未満であればボーナスが付与されます。

---

## ヒント

- `dynamodb/query_gsi.py` の GSI に対する `query` を参考にしてください。`ScanIndexForward` パラメータでソート順を制御できます
  ```python
  response = ddb_client.query(
      TableName=table_name,
      IndexName=index_name,
      KeyConditionExpression="gameId = :gameId",
      ExpressionAttributeValues={
          ":gameId": {"S": target_game_id}
      },
      ScanIndexForward=False,  # ソートキー降順
  )
  items = response["Items"]
  ```

- DynamoDB の `query` 結果は**常にソートキーの値順**で返されます（[API リファレンス](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html)）。`ScanIndexForward=False` を指定すると降順になります

- DynamoDB の型付きデータを通常の Python の値に変換するには `TypeDeserializer` を使います
  ```python
  from boto3.dynamodb.types import TypeDeserializer
  deserializer = TypeDeserializer()
  data = {key: deserializer.deserialize(value) for key, value in item.items()}
  ```

- `dynamodb/update_item.py` の条件付き更新を参考にしてください。条件を満たさない場合は `ConditionalCheckFailedException` が発生します
  ```python
  try:
      response = ddb_client.update_item(
          TableName=table_name,
          Key={
              "userId": {"N": str(user_id)},
              "gameId": {"S": game_id},
          },
          UpdateExpression="SET life = life + :add_life",
          ConditionExpression="life < :max_life",
          ExpressionAttributeValues={
              ":add_life": {"N": "1"},
              ":max_life": {"N": "3"},
          },
          ReturnValues="ALL_NEW",
      )
  except ClientError as e:
      if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
          print("条件を満たさないため更新をスキップしました。")
      else:
          raise
  ```

- `s3/client02-put-object.py` の `put_object` によるオブジェクト格納を参考にしてください
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
  key = f"ranking-{target_game_id}-{timestamp}.txt"
  ```

---

## 実行方法

```bash
cd aws_sdk/challenge3
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
- DynamoDB テーブル（GSI も同時に削除されます）
