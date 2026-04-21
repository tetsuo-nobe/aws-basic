'''
Amazon Bedrock Converse API のサンプル

Amazon Nova Lite に対して Converse API で複数ターンの会話を行うサンプルです。
1回目のリクエストで質問し、レスポンスを会話履歴に追加したうえで
2回目のリクエストを送ることで、文脈を踏まえた回答を得られます。

前提条件:
  - boto3 がインストール済みであること（pip install boto3）
  - AWS の認証情報が設定済みであること
  - Amazon Bedrock で us.amazon.nova-lite-v1:0 モデルが使用できること

実行方法:
  python converse_api.py
'''

import boto3

# Bedrock Runtime クライアントを作成
bedrock_client = boto3.client('bedrock-runtime')

# 使用するモデル ID
model_id = "us.amazon.nova-lite-v1:0"

# 推論パラメータ
inference_config = {"temperature": 0.5}

# システムプロンプト（モデルの役割を定義）
system_prompts = [
    {"text": "あなたは日本の文化や歴史に詳しいガイドです。質問に対して丁寧にわかりやすく日本語で回答してください。"}
]

# 会話履歴を保持するリスト
messages = []

# --- 1回目のリクエスト ---
message_1 = {
    "role": "user",
    "content": [{"text": "日本の四季それぞれの代表的な行事や風物詩を教えてください。"}]
}
messages.append(message_1)

response = bedrock_client.converse(
    modelId=model_id,
    messages=messages,
    system=system_prompts,
    inferenceConfig=inference_config
)

# レスポンスを会話履歴に追加
output_message = response['output']['message']
messages.append(output_message)

# --- 2回目のリクエスト（1回目の回答を踏まえた追加質問） ---
message_2 = {
    "role": "user",
    "content": [{"text": "その中でも特に秋の行事について、由来や楽しみ方を詳しく教えてください。"}]
}
messages.append(message_2)

response = bedrock_client.converse(
    modelId=model_id,
    messages=messages,
    system=system_prompts,
    inferenceConfig=inference_config
)

output_message = response['output']['message']
messages.append(output_message)

# --- 会話全体を表示 ---
for message in messages:
    print(f"Role: {message['role']}")
    for content in message['content']:
        print(f"Text: {content['text']}")
    print()
