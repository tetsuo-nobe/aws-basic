# Amazon DynamoDB 操作サンプル

DynamoDB Client API を使用したテーブル・アイテム操作のサンプルです。ゲームのスコア情報を管理するテーブルを作成し、アイテムの CRUD 操作やグローバルセカンダリインデックス（GSI）を使ったクエリを体験できます。

## 前提条件

- Python 3 がインストール済みであること
- boto3 がインストール済みであること（`pip3 install boto3`）
- AWS の認証情報が設定済みであること
- 利用するリージョンは us-west-2 (オレゴン)

---

## テーブル設計

### テーブル: `score`

| キー | 属性名 | 型 | 説明 |
|------|--------|-----|------|
| パーティションキー | `userId` | 数値 (N) | ユーザーの ID |
| ソートキー | `gameId` | 文字列 (S) | ゲームの ID |

その他の属性: `score`（数値）、`life`（数値）

### GSI: `game_index`

| キー | 属性名 | 型 | 説明 |
|------|--------|-----|------|
| パーティションキー | `gameId` | 文字列 (S) | ゲームの ID |
| ソートキー | `score` | 数値 (N) | スコア |

### サンプルデータ（`score_data.json`）

| userId | gameId | score | life |
|--------|--------|-------|------|
| 1 | G001 | 1000 | 1 |
| 1 | G002 | 2000 | 2 |
| 1 | G003 | 3000 | 3 |
| 2 | G001 | 1100 | 2 |
| 2 | G002 | 1200 | 1 |
| 2 | G003 | 1300 | 3 |
| 3 | G001 | 3100 | 3 |
| 3 | G002 | 3200 | 2 |
| 3 | G003 | 3300 | 1 |
| 3 | G004 | 3400 | 2 |

---

## ファイル一覧

| ファイル名 | 概要 |
|-----------|------|
| `myconfig.py` | テーブル名・インデックス名を定義する共通設定ファイル |
| `score_data.json` | テーブルにロードするサンプルデータ（JSON） |
| `create_table.py` | テーブルを作成する（パーティションキー: `userId`、ソートキー: `gameId`） |
| `put_item.py` | `put_item` で `score_data.json` のデータをテーブルにロードする |
| `get_item.py` | `get_item` でプライマリキーを指定してアイテムを取得する（結果整合性・強力な整合性・射影） |
| `query.py` | `query` でパーティションキー（`userId`）を指定してアイテムを検索する |
| `update_item.py` | `update_item` で条件付き更新を行う（スコアが 3000 以上なら `life` を増加） |
| `add_gsi.py` | グローバルセカンダリインデックス（GSI）を作成する |
| `query_gsi.py` | GSI に対して `query` を実行する（`gameId` とスコアの範囲で検索） |
| `delete_item.py` | `delete_item` でプライマリキーを指定してアイテムを削除する |
| `delete_table.py` | `delete_table` でテーブルを削除する |

---

## 実行順序

以下の順序で実行することで、DynamoDB の基本操作を一通り体験できます。

```bash
cd aws_sdk/dynamodb

# 1. テーブルを作成
python3 create_table.py

# 2. サンプルデータをロード
python3 put_item.py

# 3. アイテムを取得（結果整合性・強力な整合性・射影）
python3 get_item.py

# 4. パーティションキーでクエリ
python3 query.py

# 5. 条件付きでアイテムを更新
python3 update_item.py

# 6. GSI を作成（数分かかります）
python3 add_gsi.py

# 7. GSI に対してクエリ
python3 query_gsi.py

# 8. アイテムを削除
python3 delete_item.py

# 9. テーブルを削除
python3 delete_table.py

```

---

## 学習ポイント

| テーマ | 内容 |
|--------|------|
| テーブル作成 | パーティションキーとソートキーを指定してテーブルを作成する |
| `put_item` | JSON ファイルからデータを読み込んでテーブルにロードする |
| `get_item` | プライマリキーを指定して単一アイテムを取得する。結果整合性と強力な整合性の違い |
| `query` | パーティションキーを指定して複数アイテムを効率的に検索する |
| `update_item` | `ConditionExpression` を使った条件付き更新 |
| `delete_item` | プライマリキーを指定してアイテムを削除する |
| テーブル削除 | テーブルを削除する |
| GSI | テーブルとは異なるキーでクエリを実行するためのセカンダリインデックス |
