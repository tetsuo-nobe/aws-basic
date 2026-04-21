# AWS SDK for Python (boto3) サンプルコード

AWS SDK for Python (boto3) を使用した各サービスの操作サンプル集です。

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- 利用するリージョンは us-west-2 (オレゴン)

---

## セットアップ

### 1. リポジトリをクローンする

```bash
git clone https://github.com/tetsuo-nobe/aws-python-basic.git
```

### 2. boto3 をインストールする

```bash
pip3 install boto3
```

---

## フォルダ構成

```
aws_sdk/
├── s3/          ... Amazon S3 の操作サンプル
├── dynamodb/    ... Amazon DynamoDB の操作サンプル
├── bedrock/     ... Amazon Bedrock の操作サンプル
├── challenge1/  ... プログラミング課題 1（Bedrock × S3 連携）
├── challenge2/  ... プログラミング課題 2（DynamoDB × S3 連携）
└── README.md
```

各フォルダの詳細は、フォルダ内の README.md を参照してください。
