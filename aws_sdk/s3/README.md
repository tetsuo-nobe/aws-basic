# Amazon S3 操作サンプル

S3 Client API を使用したバケット・オブジェクト操作のサンプルです。ファイル名の番号順に実行することで、バケットの作成からオブジェクト操作、削除までの一連の流れを体験できます。

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- 利用するリージョンは us-west-2 (オレゴン)

---

## 事前準備

`mybucket.py` の `bucket_name` を自分のバケット名に変更してください。バケット名はグローバルで一意である必要があります。

```python
# mybucket.py
bucket_name = 'notes-bucket-xxxxxxxx'  # ← 自分のユニークなバケット名に変更
```

> バケット名の接頭辞は `notes-bucket-` にしてください。

---

## ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `mybucket.py` | バケット名を定義する共通設定ファイル（各サンプルから import される） |
| `client01-create-bucket.py` | バケットを作成する |
| `client02-put-object.py` | `put_object` でオブジェクト（`cat.jpg`）をバケットに格納する |
| `client03-upload-file.py` | `upload_file` でファイル（`Eiffel.jpg`）をバケットにアップロードする |
| `client04-get-object.py` | `get_object` でオブジェクト（`cat.jpg`）を取得しローカルに保存する |
| `client05-download-file.py` | `download_file` でオブジェクト（`Eiffel.jpg`）をダウンロードする |
| `client08-delete-object.py` | オブジェクト（`Eiffel.jpg`）を削除する |
| `client11-presigned_url.py` | 署名付き URL を生成する（有効期限 30 秒） |
| `client12-delete-bucket.py` | バケット内の全オブジェクトを削除した後、バケットを削除する |
| `cat.jpg` | サンプル用の画像ファイル（`client02`、`client04`、`client11` で使用） |
| `Eiffel.jpg` | サンプル用の画像ファイル（`client03`、`client05`、`client08` で使用） |

---

## 実行順序

番号順に実行することで、S3 の基本操作を一通り体験できます。

```bash
cd aws_sdk/s3

# 1. バケットを作成
python3 client01-create-bucket.py

# 2. put_object でオブジェクトを格納
python3 client02-put-object.py

# 3. upload_file でファイルをアップロード
python3 client03-upload-file.py

# 4. get_object でオブジェクトを取得
python3 client04-get-object.py

# 5. download_file でオブジェクトをダウンロード
python3 client05-download-file.py

# 6. オブジェクトを削除
python3 client08-delete-object.py

# 7. 署名付き URL を生成
python3 client11-presigned_url.py

# 8. バケットを削除（バケット内の全オブジェクトも削除される）
python3 client12-delete-bucket.py
```

---

## 学習ポイント

| テーマ | 内容 |
|--------|------|
| `put_object` と `upload_file` の違い | `put_object` はバイト列やファイルオブジェクトを直接指定、`upload_file` はファイルパスを指定する |
| `get_object` と `download_file` の違い | `get_object` はレスポンスの Body を読み取って保存、`download_file` はファイルパスを指定して直接保存する |
| 署名付き URL | 一時的な認証付きアクセスを提供する URL を生成できる |
| バケット削除 | バケット内にオブジェクトがある場合は先に削除が必要 |
