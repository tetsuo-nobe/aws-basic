'''
プログラミング課題: Bedrock × S3 連携

プロンプトを Amazon Bedrock の基盤モデルに送信し、
レスポンスを Amazon S3 バケットに保存するプログラムを作成してください。

処理の流れ:
  1. プロンプト（質問文）を文字列の変数として定義する
  2. Bedrock の Converse API で基盤モデル（us.amazon.nova-lite-v1:0）にリクエストを送信する
  3. モデルから返ってきたレスポンス（テキスト）を取得する
  4. プロンプトとレスポンスを合わせたテキストを S3 バケットにオブジェクトとして格納する
  5. 格納が完了したら、保存先のバケット名とオブジェクトキーを表示する

要件:
  - モデル ID: us.amazon.nova-lite-v1:0
  - API: Bedrock Runtime の Converse API（converse メソッド）
  - システムプロンプト: 自由に設定（例：「あなたは親切なアシスタントです。」）
  - プロンプト: 文字列の変数として定義する
  - S3 格納内容: プロンプトとレスポンスの両方を含むテキスト
  - S3 オブジェクトキー: 任意（タイムスタンプを含めると重複を避けられます）
  - エラー処理: try/except で適切にエラーハンドリングを行う

前提条件:
  - boto3 がインストール済みであること（pip install boto3）
  - AWS の認証情報が設定済みであること
  - Amazon Bedrock で us.amazon.nova-lite-v1:0 モデルが使用できること
  - S3 バケットが s3/client01-create-bucket.py で作成済みであること

ヒント:
  - converse_api.py の Converse API の呼び出し方を参考にしてください
  - s3/client02-put-object.py の put_object によるオブジェクト格納を参考にしてください
  - s3/mybucket.py からバケット名を import する際は sys.path にパスを追加してください
  - S3 の Body にはバイト列を渡す必要があります（.encode('utf-8') で変換）
  - datetime モジュールでタイムスタンプを生成できます

実行方法:
  cd aws_sdk/bedrock
  python challenge.py
'''

# ここにコードを記述してください
