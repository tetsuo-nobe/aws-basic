# ワーク: API Gateway REST API と Lambda 関数を統合してみよう

## 手順

1. 個人に割り振られた番号を確認します。この番号はリソース名に付加して、リソース名をユニークにするために使用します。

1. AWS マネジメントコンソールにサインインします。

### Lambda 関数の作成

3. AWS マネジメントコンソールで、ページ上部の検索窓で `lambda` と入力し、表示されるメニューから **Lambda** の部分をクリックします。

1. AWS Lambda のページで、左側のメニューから **関数** をクリックします。

1. Lambda 関数の作成
   - [**関数を作成**] をクリックします。
   - 下記を入力・設定します。
      - 関数名: `greeting-function-(自分の番号)`
      - ランタイム: **Python 3.14**
   - ページの右下にある [**関数を作成**] をクリックします。
   - [**Getting started**] のダイアログが表示された場合は [**Dismiss**]をクリックします。

1. Lambda 関数のコードの作成
   - コード: 下記のコードをコピーして既存のコードを置換えます。
   - ```python
     import json

     def lambda_handler(event, context):
         # API Gateway プロキシ統合から送られた body を取得
         body = json.loads(event['body'])

         # your_name の値を取得
         your_name = body['your_name']

         # 挨拶メッセージを作成
         greeting = f'こんにちは！ {your_name} さん'

         # API Gateway プロキシ統合のレスポンス形式で返す
         return {
             'statusCode': 200,
             'headers': {
                 'Content-Type': 'application/json; charset=utf-8'
             },
             'body': json.dumps({'greeting': greeting}, ensure_ascii=False)
         }
     ```
   - コード変更後は [**Deploy**] をクリックします。

1. Lambda 関数のテスト実行（API Gateway プロキシ統合形式）
   - [**テスト**] タブをクリックします。
   - [**テンプレート - オプション**] で [API Gateway AWS Proxy] を選択します。
   - [**イベント JSON**] で **body** 要素だけを下記の内容に置換えます。
      - イベント JSON: 
      ```json
      {
          "body": "{\"your_name\": \"太郎\"}",
      ```
   - [**テスト**] をクリックします。
   - 緑色の [**実行中の関数: 成功 (ログ)**] が表示されることを確認します。
   - [**詳細**] をクリックして展開表示します。
   - 下記が表示されていることを確認します。
     ```json
     {
       "statusCode": 200,
       "headers": {
         "Content-Type": "application/json; charset=utf-8"
       },
       "body": "{\"greeting\": \"こんにちは！ 太郎 さん\"}"
     }
     ```

### API Gateway REST API の作成

1. AWS マネジメントコンソールで、ページ上部の検索窓で `api gateway` と入力し、表示されるメニューから **API Gateway** をクリックします。

1. [**API の作成**] または [**API を作成**] をクリックします。

1. REST API の作成
   - API タイプの選択で **REST API** の [**構築**] をクリックします。（「REST API プライベート」ではない方）
   - 下記を入力・設定します。
      - API 名: `greeting-api-(自分の番号)`
   - [**API を作成**] をクリックします。

1. リソースの作成
   - 左側のメニューから [**リソース**] をクリックします。
   - [**リソースを作成**] をクリックします。
   - 下記を入力します。
      - リソースパス: `/`
      - リソース名: `greeting`
   - [**リソースを作成**] をクリックします。

1. POST メソッドの作成（Lambda プロキシ統合）
   - 作成した `/greeting` リソースが選択された状態で [**メソッドを作成**] をクリックします。
   - 下記を入力・設定します。
      - メソッドタイプ: **POST**
      - 統合タイプ: **Lambda 関数**
      - **Lambda プロキシ統合** をオンにします。
      - Lambda 関数: `greeting-function-(自分の番号)` を選択します。
   - [**メソッドを作成**] をクリックします。

1. API Gateway のテスト機能でテスト
   - 作成した POST メソッドのページで [**テスト**] タブをクリックします。
   - **リクエスト本文** に下記を入力します。
     ```json
     {
         "your_name": "花子"
     }
     ```
   - [**テスト**] をクリックします。
   - **レスポンス本文** に下記が表示されることを確認します。
     ```json
     {"greeting": "こんにちは！ 花子 さん"}
     ```
   - **ステータス** が `200` であることを確認します。

### API のデプロイ

13. API のデプロイ
    - [**API をデプロイ**] をクリックします。
    - 下記を入力・設定します。
       - ステージ: **新しいステージ**
       - ステージ名: `prod`
    - [**デプロイ**] をクリックします。

1. デプロイ後の URL の確認
   - デプロイ完了後、ページ上部に表示される **URL を呼び出す** の URL をコピーします。
   - この URL は `https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod` のような形式です。

### CloudShell から curl コマンドで API を呼び出す

15. AWS マネジメントコンソールの左下にある **CloudShell** のアイコンをクリックして CloudShell を起動します。

1. 下記の curl コマンドを実行します。（URL は自分の API の URL に置換えて、最後に `/greeting` をつけてください。）
   ```bash
   curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"your_name": "太郎"}' \
     https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod/greeting
   ```
   - 下記のレスポンスが返ることを確認します。
     ```json
     {"greeting": "こんにちは！ 太郎 さん"}
     ```
   - CloudShell を閉じます。

---
## クリーンアップ手順

1. API Gateway REST API の削除
   - API Gateway のコンソールで、左側のメニューから [**API**] をクリックします。
   - `greeting-api-(自分の番号)` を選択します。
   - [**API を削除**] をクリックします。
   - ダイアログで API 名を入力して確認し、削除します。
1. Lambda 関数の削除
   - AWS マネジメントコンソールで、ページ上部の検索窓で `lambda` と入力し、**Lambda** をクリックします。
   - 左側のメニューから **関数** をクリックします。
   - `greeting-function-(自分の番号)` を選択します。
   - **アクション** から **関数の削除** を選択します。
   - ダイアログで確認して削除します。
1. CloudWatch Logs のログの削除
   - AWS マネジメントコンソールで、ページ上部の検索窓で `cloudwatch` と入力し、**CloudWatch** をクリックします。
   - 左側のメニューから **ログ** > **ログ管理** をクリックします。
   - ロググループ一覧から `/aws/lambda/greeting-function-(自分の番号)` を選択（チェックボックスをオン）します。
   - **アクション** から **ロググループの削除** を選択します。
   - ダイアログで確認して削除します。
1. （オプション）Lambda 実行ロールの削除
   - この手順はオプションです。実行ロールを他の Lambda 関数で再利用しない場合に実施して下さい。
   - AWS マネジメントコンソールで、ページ上部の検索窓で `iam` と入力し、**IAM** をクリックします。
   - 左側のメニューから **ロール** をクリックします。
   - 検索窓に `greeting-function-(自分の番号)-role` を入力して検索します。
   - 該当のロールを選択（チェックボックスをオン）します。
   - [**削除**] をクリックします。
   - ダイアログでロール名を入力して確認し、削除します。
---
