'''
プログラミング課題: Bedrock × S3 連携 の解答例

プロンプトを Amazon Bedrock の基盤モデルに送信し、
レスポンスを Amazon S3 バケットに保存するプログラムです。

処理の流れ:
  1. プロンプト（質問文）を文字列の変数として定義する
  2. Bedrock の Converse API でリクエストを送信する
  3. レスポンス（テキスト）を取得する
  4. プロンプトとレスポンスを合わせて S3 に格納する
  5. 保存先のバケット名とオブジェクトキーを表示する

前提条件:
  - boto3 がインストール済みであること（pip install boto3）
  - AWS の認証情報が設定済みであること
  - Amazon Bedrock で us.amazon.nova-lite-v1:0 モデルが使用できること
  - S3 バケットが s3/client01-create-bucket.py で作成済みであること

実行方法:
  cd aws_sdk/bedrock
  python challenge_answer.py
'''

import sys
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# S3 バケット名を共通設定ファイルから import
sys.path.append('../s3')  # challenge1 フォルダから s3 フォルダへの相対パス
from mybucket import bucket_name as bucket

# --- 1. プロンプトを変数として定義 ---
prompt = "日本で一番高い山はなんですか？"

print(f"プロンプト: {prompt}")
print("Bedrock にリクエストを送信中...")

try:
    # --- 2. Bedrock Converse API でリクエストを送信 ---
    bedrock_client = boto3.client('bedrock-runtime')

    # 使用するモデル ID
    model_id = "us.amazon.nova-lite-v1:0"

    # 推論パラメータ
    inference_config = {"temperature": 0.5}

    # システムプロンプト
    system_prompts = [
        {"text": "あなたは親切なアシスタントです。質問に対して丁寧にわかりやすく日本語で回答してください。"}
    ]

    # ユーザーメッセージ
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ]

    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config
    )

    # --- 3. レスポンスのテキストを取得 ---
    response_text = response['output']['message']['content'][0]['text']

    print()
    print("--- Bedrock のレスポンス ---")
    print(response_text)
    print("--------------------------")

    # --- 4. プロンプトとレスポンスを S3 に格納 ---
    s3_client = boto3.client('s3')

    # 格納するテキストを組み立てる
    body_text = f"プロンプト:\n{prompt}\n\nレスポンス:\n{response_text}"

    # タイムスタンプを含めたオブジェクトキーを作成
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    key = f'bedrock-response-{timestamp}.txt'

    s3_client.put_object(
        Body=body_text.encode('utf-8'),
        Bucket=bucket,
        Key=key
    )

    # --- 5. 保存先の情報を表示 ---
    print()
    print("S3 に保存しました。")
    print(f"  バケット: {bucket}")
    print(f"  キー: {key}")

except NoCredentialsError as nocrederr:
    print("!!!! InvalidCredentials !!!!")
    print(nocrederr)
except ClientError as clienterr:
    print('!!!! ClientError !!!!')
    print(clienterr)
    error_code = clienterr.response['Error']['Code']
    print('error_code=', error_code)
except Exception as ex:
    print('!!!! Exception !!!!')
    print(ex)
