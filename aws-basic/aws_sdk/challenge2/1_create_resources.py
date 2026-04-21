"""
チャレンジ 2 の事前準備: リソースの作成

以下のリソースを作成します。
  1. DynamoDB テーブル (score) を作成する
  2. score_data.json のデータをテーブルにロードする
  3. S3 バケットを作成する

実行方法:
  cd aws_sdk/challenge2
  python 1_create_resources.py
"""
import boto3
import botocore
import json
from myconfig import table_name, bucket_name


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


def create_s3_bucket():
    """S3 バケットを作成する"""
    s3_client = boto3.client("s3")

    print(f"S3 バケット '{bucket_name}' を作成中...")
    create_bucket_config = {"LocationConstraint": "us-west-2"}
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
        create_s3_bucket()
        print()
        print("===== 事前準備が完了しました =====")
        print(f"  DynamoDB テーブル: {table_name}")
        print(f"  S3 バケット: {bucket_name}")
    except botocore.exceptions.ClientError as err:
        print("!!!! ClientError !!!!")
        print(err.response["Error"]["Message"])
    except Exception as ex:
        print("!!!! Exception !!!!")
        print(ex)
