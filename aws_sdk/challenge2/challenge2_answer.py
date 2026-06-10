"""
プログラミング課題 2: DynamoDB × S3 連携（スコアレポート生成）の解答例

DynamoDB テーブルから特定ユーザーのスコアデータを検索し、
テキストレポートを作成して S3 バケットに保存し、
署名付き URL を生成して表示するプログラムです。

前提条件:
  - boto3 がインストール済みであること（pip install boto3）
  - AWS の認証情報が設定済みであること
  - 1_create_resources.py でリソースが作成済みであること

実行方法:
  cd aws_sdk/challenge2
  python challenge_answer.py
"""
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer
from myconfig import table_name, bucket_name

# 検索対象のユーザー ID
target_user_id = 3

try:
    # --- 1. DynamoDB から特定ユーザーのスコアデータを取得 ---
    ddb_client = boto3.client("dynamodb")

    print(f"DynamoDB テーブル '{table_name}' から userId={target_user_id} のデータを検索中...")

    response = ddb_client.query(
        TableName=table_name,
        KeyConditionExpression="userId = :userId",
        ExpressionAttributeValues={
            ":userId": {"N": str(target_user_id)}
        },
    )

    items = response["Items"]
    print(f"{len(items)} 件のアイテムを取得しました。")

    # DynamoDB の型付きデータを通常の Python 辞書に変換するユーティリティ
    deserializer = TypeDeserializer()

    def deserialize_item(item):
        return {key: deserializer.deserialize(value) for key, value in item.items()}

    # --- 2. テキストレポートを作成 ---
    report_lines = []
    report_lines.append("=" * 40)
    report_lines.append(f"  スコアレポート (userId: {target_user_id})")
    report_lines.append(f"  作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 40)
    report_lines.append("")

    for item in items:
        data = deserialize_item(item)
        report_lines.append(f"  ゲーム ID : {data['gameId']}")
        report_lines.append(f"  スコア   : {data['score']}")
        report_lines.append(f"  ライフ   : {data['life']}")
        report_lines.append("-" * 40)

    report_lines.append("")
    report_lines.append(f"  合計ゲーム数: {len(items)}")
    report_lines.append("=" * 40)

    report_text = "\n".join(report_lines)

    print()
    print("--- 生成されたレポート ---")
    print(report_text)
    print("--------------------------")

    # --- 3. レポートを S3 バケットに保存 ---
    s3_client = boto3.client("s3")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    key = f"score-report-user{target_user_id}-{timestamp}.txt"

    s3_client.put_object(
        Body=report_text.encode("utf-8"),
        Bucket=bucket_name,
        Key=key,
    )

    print()
    print("S3 に保存しました。")
    print(f"  バケット: {bucket_name}")
    print(f"  キー: {key}")

    # --- 4. 署名付き URL を生成して表示 ---
    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=60,
        HttpMethod="GET",
    )

    print()
    print("署名付き URL（有効期限: 60 秒）:")
    print(f"  {url}")

except ClientError as clienterr:
    print("!!!! ClientError !!!!")
    print(clienterr.response["Error"]["Message"])
except Exception as ex:
    print("!!!! Exception !!!!")
    print(ex)
