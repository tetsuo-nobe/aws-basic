# ワーク: AWS Lambda 関数を作成してテスト実行してみよう

## 手順

1. 個人に割り振られた番号を確認します。

1. AWS マネジメントコンソールにサインします。

1. AWS マネジメントコンソールで、ページ上部の検索窓で `lambda` と入力し、表示されるメニューから **Lambda** の部分をクリックします。 

1. AWS Lambda のページで、左側のメニューから **関数** をクリックします。

1. Lambda 関数の作成
   - [**関数を作成**] をクリックします。
   - 下記を入力・設定します。
      - 関数名: `my-function-(自分の番号)`
      - ランタイム: **Python 3.14**
   - ページの右下にある [**関数の作成**] をクリックします。
   - [**Getting started**] のダイアログが表示された場合は [**Dismiss**]をクリックします。
1. Lambda 関数のコードの作成
   - コード: 下記のコードをコピーして既存のコードを置換えます。
   - ```python
     from datetime import datetime
     import os

     # ハンドラ関数の外側で日時データを取得
     outside_handler = datetime.now()

     def lambda_handler(event, context):
         # ハンドラ関数の内側で日時データを取得
         inside_handler = datetime.now()  
    
         # 取得した日時データをログ出力
         print('outside_handler :' + str(outside_handler))
         print('inside_handler  :' + str(inside_handler))
    
         # 環境変数 MSG から値を取得
         message = os.environ.get('MSG', 'Hello')
    
         # context オブジェクトからいくつかの値をログ出力
         print("Lambda function ARN:", context.invoked_function_arn)
         print("Lambda Request ID:", context.aws_request_id)
         print("Lambda function memory limits in MB:", context.memory_limit_in_mb)
    
         # event オブジェクトから name の値を取得して return のペイロードに含める
         return {
             'statusCode': 200,
             'body': message + ' '  + event['name']
             }
     ```
   - コード変更後は [**Deploy**] をクリック
1. Lambda 関数の環境変数を設定
   - [**設定**] タブをクリックします。
   - 左側メニューより[**環境変数**] をクリックします。
   - [**編集**] をクリックします。
   - [**環境変数の追加**] をクリックします。
   - [**キー**] に `MSG` 、[**値**] に `Hello!` を入力します。
   - [**保存**] をクリックします。
1. Lambda 関数のテスト実行
   - [**テスト**] タブをクリックします。
   - 下記を入力・設定します。   
      - イベント JSON:下記の内容に置換えます。
      ```json
      {
          "name": "Alex"
      }
      ```
   - [**テスト**] をクリックします。
   - 緑色の [**実行中の関数: 成功 (ログ)**] が表示されることを確認します。
   - [**詳細**]をクリックして展開表示します。
   - 下記が表示されていることを確認します。
     ```json
     {
       "statusCode": 200,
       "body": "Hello! Alex"
     }
     ```
   - [**ログ出力**] セクションを確認します。
   - その後、数回 [**テスト**] をクリックします。
      - テスト実行する毎に、[**ログ出力**] の [**outside_handler**] と [**inside_handler**] の値がどうなるかを確認します。

1. Lambda 関数の実行ロールの確認
   - Lambda 関数のページで [**設定**] タブをクリックします。
   - 左側メニューより [**アクセス権限**] をクリックします。
   - **実行ロール** セクションに表示されているロール名のリンクをクリックします。
   - IAM コンソールが開き、Lambda 関数に割り当てられた実行ロールの詳細が表示されます。
   - **許可ポリシー** セクションで、アタッチされているポリシーを確認します。
      - デフォルトでは **AWSLambdaBasicExecutionRole** ポリシーがアタッチされています。
      - このポリシーにより、Lambda 関数が CloudWatch Logs にログを書き込む権限が付与されています。
1. CloudWatch Logs のログを確認
  - [**モニタリング**] タブをクリックします。
  - [**CloudWatch ログを表示**] をクリックします。
  - **/aws/lambda/my-function-(自分の番号)** という名前のロググループのページが表示されることを確認します。
  -  ログストリーム名のリンクをクリックします。
  - Lambda 関数実行時のログが表示されていることを確認します。
      - Lambda 関数のコードで print 関数で出力した内容や、START、END、REPORT のログイベントが表示されることを確認します。
---
## クリーンアップ手順

1. Lambda 関数の削除
   - **Lambda 関数を削除して下さい。**
   - my-function のページの右上にある **アクション** から **関数の削除** を選択します。
   - ダイアログで確認して削除します。
1. CloudWatch Logs のログの削除
   - AWS マネジメントコンソールで、ページ上部の検索窓で `cloudwatch` と入力し、**CloudWatch** をクリックします。
   - 左側のメニューから **ログ** > **ログ管理** をクリックします。
   - ロググループ一覧から `/aws/lambda/my-function-(自分の番号)` を選択（チェックボックスをオン）します。
   - **アクション** から **ロググループの削除** を選択します。
   - ダイアログで確認して削除します。
1. （オプション）Lambda 実行ロールの削除
   - この手順はオプションです。実行ロールを他の Lambda 関数で再利用しない場合に実施して下さい。
   - AWS マネジメントコンソールで、ページ上部の検索窓で `iam` と入力し、**IAM** をクリックします。
   - 左側のメニューから **ロール** をクリックします。
   - 検索窓に Lambda 関数作成時に自動生成されたロール名（例: `my-function-(自分の番号)-role-xxxxxxxx`）を入力して検索します。
   - 該当のロールを選択（チェックボックスをオン）します。
   - [**削除**] をクリックします。
   - ダイアログでロール名を入力して確認し、削除します。
---
