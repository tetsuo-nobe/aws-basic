"""
チャレンジ 3 の事前準備: リソースの作成

以下のリソースを作成します。
  1. DynamoDB テーブル (score) を作成する
  2. score_data.json のデータをテーブルにロードする
  3. GSI (game_index) を作成する
  4. S3 バケットを作成する

実行方法:
  cd aws_sdk/challenge3
  python 1_create_resources.py
"""
import boto3
import botocore
import json
import time
from myconfig import table_name, index_name, bucket_name


def create_dynamodb_table():
    """DynamoDB テーブルを作成する"""
    ddb_client = boto3.client("dynamodb")

    print(f"DynamoDB テーブル '{table_name}' を作成中...")
    ddb_client.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "userId", "KeyType": "HASH"},
            {"AttributeName": "gameId", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "userId", "AttributeType": "N"},
            {"AttributeName": "gameId", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 3,
            "WriteCapacityUnits": 3,
        },
    )

    # テーブル作成完了まで待機
    waiter = ddb_client.get_waiter("table_exists")
    waiter.wait(TableName=table_name)
    print(f"DynamoDB テーブル '{table_name}' を作成しました。")


def load_data():
    """score_data.json のデータを DynamoDB テーブルにロードする"""
    ddb_client = boto3.client("dynamodb")

    f = open("score_data.json")
    scores = json.load(f)

    print(f"テーブル '{table_name}' にデータをロード中...")
    for rec in scores:
        item = {
            "userId": {"N": str(rec["userId"])},
            "gameId": {"S": rec["gameId"]},
            "score": {"N": str(rec["score"])},
            "life": {"N": str(rec["life"])},
        }
        ddb_client.put_item(TableName=table_name, Item=item)

    f.close()
    print(f"{len(scores)} 件のデータをロードしました。")


def create_gsi():
    """GSI (game_index) を作成する"""
    ddb_client = boto3.client("dynamodb")

    print(f"GSI '{index_name}' を作成中...")
    ddb_client.update_table(
        TableName=table_name,
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": index_name,
                    "KeySchema": [
                        {"AttributeName": "gameId", "KeyType": "HASH"},
                        {"AttributeName": "score", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 3,
                        "WriteCapacityUnits": 3,
                    },
                }
            }
        ],
        AttributeDefinitions=[
            {"AttributeName": "gameId", "AttributeType": "S"},
            {"AttributeName": "score", "AttributeType": "N"},
        ],
    )

    # GSI 作成完了まで待機（waiter が使えないためポーリング）
    index_status = ""
    while index_status != "ACTIVE":
        time.sleep(15)
        response = ddb_client.describe_table(TableName=table_name)
        gsi_list = response["Table"].get("GlobalSecondaryIndexes", [])
        if gsi_list:
            index_status = gsi_list[0]["IndexStatus"]
        print(f"  GSI ステータス: {index_status}（ACTIVE になるまで待機中...）")

    print(f"GSI '{index_name}' を作成しました。")


def create_s3_bucket():
    """S3 バケットを作成する"""
    s3_client = boto3.client("s3")

    print(f"S3 バケット '{bucket_name}' を作成中...")
    create_bucket_config = {"LocationConstraint": "ap-northeast-1"}
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration=create_bucket_config,
    )

    waiter = s3_client.get_waiter("bucket_exists")
    waiter.wait(Bucket=bucket_name)
    print(f"S3 バケット '{bucket_name}' を作成しました。")


if __name__ == "__main__":
    try:
        create_dynamodb_table()
        load_data()
        create_gsi()
        create_s3_bucket()
        print()
        print("===== 事前準備が完了しました =====")
        print(f"  DynamoDB テーブル: {table_name}")
        print(f"  GSI: {index_name}")
        print(f"  S3 バケット: {bucket_name}")
    except botocore.exceptions.ClientError as err:
        print("!!!! ClientError !!!!")
        print(err.response["Error"]["Message"])
    except Exception as ex:
        print("!!!! Exception !!!!")
        print(ex)
