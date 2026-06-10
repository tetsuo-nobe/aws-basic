"""
プログラミング課題 3: DynamoDB GSI × S3 連携（ゲームランキング生成＆条件付きボーナス付与）の解答例

DynamoDB の GSI を使ってゲームのスコアランキングを取得し、
1位のプレイヤーに条件付きでボーナスライフを付与した後、
ランキングレポートを S3 に保存して署名付き URL を生成するプログラムです。

前提条件:
  - boto3 がインストール済みであること（pip install boto3）
  - AWS の認証情報が設定済みであること
  - 1_create_resources.py でリソースが作成済みであること

実行方法:
  cd aws_sdk/challenge3
  python challenge_answer.py
"""
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer
from myconfig import table_name, index_name, bucket_name

# ランキングを取得するゲーム ID
target_game_id = "G001"

try:
    # --- 1. GSI に対して query を実行し、スコア降順でランキングを取得 ---
    ddb_client = boto3.client("dynamodb")
    deserializer = TypeDeserializer()

    print(f"ゲーム '{target_game_id}' のランキングを取得中...（スコア降順）")

    response = ddb_client.query(
        TableName=table_name,
        IndexName=index_name,
        KeyConditionExpression="gameId = :gameId",
        ExpressionAttributeValues={
            ":gameId": {"S": target_game_id}
        },
        ScanIndexForward=False,  # スコア降順（ランキング順）
    )

    items = response["Items"]
    print(f"{len(items)} 件のアイテムを取得しました。")

    # DynamoDB の型付きデータを通常の Python 辞書に変換
    def deserialize_item(item):
        return {key: deserializer.deserialize(value) for key, value in item.items()}

    # ランキングデータを変換
    ranking = [deserialize_item(item) for item in items]

    # ランキング表示
    print()
    print(f"--- {target_game_id} ランキング ---")
    for i, player in enumerate(ranking, 1):
        print(f"  {i}位: userId={int(player['userId'])}, スコア={int(player['score'])}, ライフ={int(player['life'])}")
    print("-" * 30)

    # --- 2. 1位のプレイヤーに条件付きでボーナスライフを付与 ---
    top_player = ranking[0]
    top_user_id = int(top_player["userId"])
    top_game_id = target_game_id

    print()
    print(f"1位のプレイヤー (userId={top_user_id}) にボーナスライフを付与中...")
    print(f"  条件: ライフが 3 未満の場合のみ +1")

    try:
        update_response = ddb_client.update_item(
            TableName=table_name,
            Key={
                "userId": {"N": str(top_user_id)},
                "gameId": {"S": top_game_id},
            },
            UpdateExpression="SET life = life + :add_life",
            ConditionExpression="life < :max_life",
            ExpressionAttributeValues={
                ":add_life": {"N": "1"},
                ":max_life": {"N": "3"},
            },
            ReturnValues="ALL_NEW",
        )
        updated_item = deserialize_item(update_response["Attributes"])
        print(f"  結果: ボーナスを付与しました！ ライフ: {int(updated_item['life'])}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(f"  結果: 条件を満たさないため更新をスキップしました。（ライフが既に 3 以上）")
        else:
            raise

    # --- 3. ランキング結果をテキストレポートとして整形 ---
    report_lines = []
    report_lines.append("=" * 40)
    report_lines.append(f"  ゲームランキングレポート ({target_game_id})")
    report_lines.append(f"  作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 40)
    report_lines.append("")

    for i, player in enumerate(ranking, 1):
        report_lines.append(f"  {i}位")
        report_lines.append(f"    ユーザー ID : {int(player['userId'])}")
        report_lines.append(f"    スコア     : {int(player['score'])}")
        report_lines.append(f"    ライフ     : {int(player['life'])}")
        report_lines.append("-" * 40)

    report_lines.append("")
    report_lines.append(f"  参加プレイヤー数: {len(ranking)}")
    report_lines.append("=" * 40)

    report_text = "\n".join(report_lines)

    print()
    print("--- 生成されたレポート ---")
    print(report_text)
    print("--------------------------")

    # --- 4. レポートを S3 バケットに保存 ---
    s3_client = boto3.client("s3")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    key = f"ranking-{target_game_id}-{timestamp}.txt"

    s3_client.put_object(
        Body=report_text.encode("utf-8"),
        Bucket=bucket_name,
        Key=key,
    )

    print()
    print("S3 に保存しました。")
    print(f"  バケット: {bucket_name}")
    print(f"  キー: {key}")

    # --- 5. 署名付き URL を生成して表示 ---
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
