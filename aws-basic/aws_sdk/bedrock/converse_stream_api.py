'''
Amazon Bedrock Converse Stream API のサンプル

Amazon Nova Lite に対して Converse API のストリーミング版を使用し、
レスポンスをリアルタイムに受信・表示するサンプルです。
通常の Converse API ではレスポンス全体が返るまで待ちますが、
ストリーミング版ではテキストが生成されるたびに逐次表示されます。

前提条件:
  - boto3 がインストール済みであること（pip install boto3）
  - AWS の認証情報が設定済みであること
  - Amazon Bedrock で us.amazon.nova-lite-v1:0 モデルが使用できること

実行方法:
  python converse_stream_api.py
'''

import boto3


def print_stream(stream):
    """ストリームのイベントを受信して表示する関数"""

    if stream:
        for event in stream:

            # メッセージの開始（ロールの表示）
            if 'messageStart' in event:
                print(f"\nRole: {event['messageStart']['role']}")

            # テキストの断片を逐次表示
            if 'contentBlockDelta' in event:
                print(event['contentBlockDelta']['delta']['text'], end="")

            # メッセージの終了（停止理由の表示）
            if 'messageStop' in event:
                print(f"\nStop reason: {event['messageStop']['stopReason']}")

            # メタデータ（トークン使用量・レイテンシ）の表示
            if 'metadata' in event:
                metadata = event['metadata']
                if 'usage' in metadata:
                    print("\nToken usage")
                    print(f"  Input tokens: {metadata['usage']['inputTokens']}")
                    print(f"  Output tokens: {metadata['usage']['outputTokens']}")
                    print(f"  Total tokens: {metadata['usage']['totalTokens']}")
                if 'metrics' in metadata:
                    print(f"  Latency: {metadata['metrics']['latencyMs']} milliseconds")


# Bedrock Runtime クライアントを作成
bedrock_client = boto3.client('bedrock-runtime')

# 使用するモデル ID
model_id = "us.amazon.nova-lite-v1:0"

# 推論パラメータ
inference_config = {"temperature": 0.5}

# システムプロンプト（モデルの役割を定義）
system_prompts = [
    {"text": "あなたは日本の食文化に詳しい料理研究家です。質問に対して丁寧にわかりやすく日本語で回答してください。"}
]

# ユーザーメッセージ
message_1 = {
    "role": "user",
    "content": [{"text": "日本各地の代表的なご当地ラーメンの特徴を、スープや麺の違いも含めて詳しく紹介してください。"}]
}

messages = [message_1]

# ストリーミングでリクエストを送信
response = bedrock_client.converse_stream(
    modelId=model_id,
    messages=messages,
    system=system_prompts,
    inferenceConfig=inference_config
)

stream = response.get('stream')

# ストリームを表示
print_stream(stream)
