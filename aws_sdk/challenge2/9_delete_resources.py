"""
チャレンジ 2 のクリーンアップ: リソースの削除

以下のリソースを削除します。
  1. S3 バケット内の全オブジェクトを削除し、バケットを削除する
  2. DynamoDB テーブルを削除する

実行方法:
  cd aws_sdk/challenge2
  python 9_delete_resources.py
"""
import boto3
import botocore
from myconfig import table_name, bucket_name


def delete_s3_bucket():
    """S3 バケット内の全オブジェクトを削除し、バケットを削除する"""
    s3_client = boto3.client("s3")

    # バケット内の全オブジェクトを削除
    print(f"S3 バケット '{bucket_name}' 内のオブジェクトを削除中...")
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    key_count = response["KeyCount"]
    if key_count > 0:
        s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={
                "Objects": [
                    {"Key": obj["Key"]} for obj in response["Contents"]
                ]
            },
        )
        print(f"  {key_count} 件のオブジェクトを削除しました。")

    # バケットを削除
    print(f"S3 バケット '{bucket_name}' を削除中...")
    s3_client.delete_bucket(Bucket=bucket_name)
    waiter = s3_client.get_waiter("bucket_not_exists")
    waiter.wait(Bucket=bucket_name)
    print(f"S3 バケット '{bucket_name}' を削除しました。")


def delete_dynamodb_table():
    """DynamoDB テーブルを削除する"""
    ddb_client = boto3.client("dynamodb")

    print(f"DynamoDB テーブル '{table_name}' を削除中...")
    ddb_client.delete_table(TableName=table_name)

    waiter = ddb_client.get_waiter("table_not_exists")
    waiter.wait(TableName=table_name)
    print(f"DynamoDB テーブル '{table_name}' を削除しました。")


if __name__ == "__main__":
    try:
        delete_s3_bucket()
        delete_dynamodb_table()
        print()
        print("===== クリーンアップが完了しました =====")
    except botocore.exceptions.ClientError as err:
        print("!!!! ClientError !!!!")
        print(err.response["Error"]["Message"])
    except Exception as ex:
        print("!!!! Exception !!!!")
        print(ex)
