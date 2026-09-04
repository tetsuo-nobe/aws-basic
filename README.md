# aws-basic
AWS の基礎のハンズオン

AWS 初心者向けに、マネジメントコンソールや AWS SDK を使った基礎的なハンズオンをまとめています。

---

## ハンズオン一覧

| ハンズオン | 内容 |
|-----------|------|
| [EC2 インスタンス作成](./compute/ec2/README.md) | EC2 インスタンスを作成し、Session Manager で接続して Web アプリを動かす |
| [AWS Lambda 関数作成](./compute/lambda/README.md) | サーバーレスな Lambda 関数を作成する |
| [Amazon S3](./s3/README.md) | バケット作成、オブジェクトのアップロード、パブリックアクセスの設定 |
| [VPC 作成](./vpc/README.md) | VPC・Public サブネットを作成し、Public サブネット上に Web サーバーを構築する |
| [ELB (Application Load Balancer)](./elb/README.md) | CloudFormation で構築した 2つの EC2 インスタンスに ALB で負荷分散する |

> 各ハンズオンは独立して実施できます。ネットワークやロードバランサーの理解を深めたい場合は、EC2 → VPC → ELB の順に進めるのがおすすめです。

---

## AWS SDK のハンズオン用に開発環境を作成する場合、以下の手順を実施して下さい。

1. インストラクターより提示された **2桁の番号** を覚えておいてください。

1. AWS マネジメントコンソールにサインインして、**東京 (ap-northeast-1) リージョン**に切り替えます。
    - インストラクターより提示された AWS アカウントと ID でサインインして下さい。

1. ページ上部の **検索** に `cfn` を入力して Enter キーを押下します。

1. AWS CloudFormation のページの左側のナビゲーションメニューで **スタック** をクリックします。

1. **スタックの作成** から **新しいリソースを使用（標準）** を選択します。

1. **テンプレートの指定** セクションで **テンプレートソース** に **Amazon S3 URL** を選択します。

1. **Amazon S3 URL** に下記を入力します。
    - `https://tnobep-work-public.s3.ap-northeast-1.amazonaws.com/bedrock-work/VSCodeServerTemplate.yaml`

1. **次へ** をクリックします。

1. **スタック名** に `vscode-server-stack-99` と入力します。
    - **99 の部分は自分の番号に置き換えてください。**
 
1. **次へ** をクリックします。

1. ページ下部で、下記のチェックボックスをチェックします。
    - 「AWS CloudFormation によって IAM リソースが作成される場合があることを承認します。」

1. さらに **次へ** をクリックします。

1. **送信** をクリックします。

1. スタックの作成が完了するまで待ちます。(約 10分 ～ 15分ほどかかります。)

1. **出力**　タブを選択します。

1. **LabWorkspacePassword** で表示されているパスワードの値をメモしておきます。

1. **LabWorkspaceURL** の値のリンクを選択します。

1. メモしておいたパスワードを入力して SUBMIT を選択し、VS Code Server を表示します。

1. VS Code Server の下部のターミナルで下記を実行し、このリポジトリを取得します。
    - もしターミナルが表示されない場合は、左上の三本線メニューから **Terminal** - **New Terminal** を選択します。
    - ```
      git clone https://github.com/tetsuo-nobe/aws-basic.git
      ```
    - ```
      cd aws-basic
      ```
      

