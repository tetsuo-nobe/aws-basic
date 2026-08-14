# IAM ハンズオン環境セットアップ手順


## AWS CloudFormation を使用する場合は下記

* Linux / macOS / CloudShell の場合
```bash
export PASSWD=Demo@0000

aws cloudformation create-stack \
  --stack-name iam-handson-stack \
  --template-body file://cfn-template.yaml \
  --parameters \
    ParameterKey=UserPassword,ParameterValue="${PASSWD}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --profile default \
  --region ap-northeast-1
```

* Windows PowerShell の場合
```powershell
$PASSWD = "Demo@0000"

aws cloudformation create-stack `
  --stack-name iam-handson-stack `
  --template-body file://cfn-template.yaml `
  --parameters `
    ParameterKey=UserPassword,ParameterValue="$PASSWD" `
  --capabilities CAPABILITY_NAMED_IAM `
  --profile default `
  --region ap-northeast-1
```

* スタック削除時は下記を実行

```
aws cloudformation delete-stack --stack-name iam-handson-stack --profile default --region ap-northeast-1
```

## AWS CLI を使用して作成する場合は下記

## 前提条件

- AWS CLI がインストール・設定済みであること
- IAM の管理権限を持つユーザーまたはロールで実行すること
- `allmost_readonly.json` と `lambda_policy.json` が手元にあること

---

## 1. IAM グループの作成

```bash
aws iam create-group --group-name demo-group1
aws iam create-group --group-name demo-group2
```

---

## 2. IAM ユーザーの作成とコンソールログインの有効化

### 2-1. ユーザーの作成

```bash
aws iam create-user --user-name demo-user1
aws iam create-user --user-name demo-user2
```

### 2-2. コンソールサインインを許可する

```bash
aws iam create-login-profile --user-name demo-user1 --password "Demo@0615" --no-password-reset-required
aws iam create-login-profile --user-name demo-user2 --password "Demo@0615" --no-password-reset-required
```

---

## 3. ユーザーをグループに追加

```bash
aws iam add-user-to-group --user-name demo-user1 --group-name demo-group1
aws iam add-user-to-group --user-name demo-user2 --group-name demo-group2
```

---

## 4. ポリシーとロールの作成、グループへの付与

### 4-0. AWS 認証情報を環境変数に設定する

```bash
export AWS_ACCESS_KEY_ID=<アクセスキーIDを入力>
export AWS_SECRET_ACCESS_KEY=<シークレットアクセスキーを入力>
export AWS_DEFAULT_REGION=ap-northeast-1
```

### 4-1. アカウント ID を環境変数に設定する

Linux / macOS / CloudShell の場合:

```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

確認:

```bash
echo $AWS_ACCOUNT_ID
```

### 4-2. allmost_readonly ポリシーを作成し demo-group1 に付与

```bash
aws iam create-policy --policy-name allmost-readonly-policy --policy-document file://allmost_readonly.json
```

```bash
aws iam attach-group-policy --group-name demo-group1 --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/allmost-readonly-policy
```

### 4-3. lambda_policy ポリシーを作成し、allmost_readonly ポリシーとともに demo-group2 に付与

```bash
aws iam create-policy --policy-name lambda-handson-policy --policy-document file://lambda_policy.json
```

```bash
aws iam attach-group-policy --group-name demo-group2 --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/lambda-handson-policy
aws iam attach-group-policy --group-name demo-group2 --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/allmost-readonly-policy
```

### 4-4. Lambda 実行ロールを作成する

ハンズオンで Lambda 関数を作成する際に指定する実行ロールを作成します。

```bash
cat <<EOF > trust-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
```

```bash
aws iam create-role \
  --role-name lambda-handson-execution-role \
  --assume-role-policy-document file://trust-policy.json
```

```bash
aws iam attach-role-policy \
  --role-name lambda-handson-execution-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

---

## 5. 設定の確認

### グループに所属するユーザーの確認

```bash
aws iam get-group --group-name demo-group1
aws iam get-group --group-name demo-group2
```

### グループにアタッチされたポリシーの確認

```bash
aws iam list-attached-group-policies --group-name demo-group1
aws iam list-attached-group-policies --group-name demo-group2
```

---

## 6. クリーンアップ（すべて削除）

ハンズオン終了後、作成したリソースをすべて削除します。  
削除は依存関係の順序（ポリシーのデタッチ → ユーザーのグループ除外 → ユーザー削除 → グループ削除 → ロール削除 → ポリシー削除）で行います。

### 6-1. グループからポリシーをデタッチする

```bash
aws iam detach-group-policy --group-name demo-group1 --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/allmost-readonly-policy
aws iam detach-group-policy --group-name demo-group2 --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/lambda-handson-policy
aws iam detach-group-policy --group-name demo-group2 --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/allmost-readonly-policy
```

### 6-2. グループからユーザーを除外する

```bash
aws iam remove-user-from-group --user-name demo-user1 --group-name demo-group1
aws iam remove-user-from-group --user-name demo-user2 --group-name demo-group2
```

### 6-3. ユーザーのログインプロファイルを削除する

```bash
aws iam delete-login-profile --user-name demo-user1
aws iam delete-login-profile --user-name demo-user2
```

### 6-4. ユーザーを削除する

```bash
aws iam delete-user --user-name demo-user1
aws iam delete-user --user-name demo-user2
```

### 6-5. グループを削除する

```bash
aws iam delete-group --group-name demo-group1
aws iam delete-group --group-name demo-group2
```

### 6-6. Lambda 実行ロールを削除する

```bash
aws iam detach-role-policy \
  --role-name lambda-handson-execution-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam delete-role --role-name lambda-handson-execution-role
```

### 6-7. ポリシーを削除する

```bash
aws iam delete-policy --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/allmost-readonly-policy
aws iam delete-policy --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/lambda-handson-policy
```

### 6-8. 一時ファイルを削除する

```bash
rm -f trust-policy.json
```
