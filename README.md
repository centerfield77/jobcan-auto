# ジョブカンの自動打刻

Cloud Schedulerで指定の時間に打刻します  
祝日はスキップします

## セットアップ
### git clone + chrome driverのダウンロード

```
git clone https://github.com/centerfield77/jobcan-auto.git
```

```
./prepareChromeDriver.sh   
```

### Google Cloudでプロジェクト作成
- サービスアカウントを作成し、キー(json)をローカルに保存する。
- 「編集者」「Project IAM 管理者」「Secret Manager 管理者」のロールを割り当てる
- 以下のAPIを有効化します
  - Cloud Functions
  - Cloud Resource Manager

### デプロイ
```
terraform init   
terraform apply                   
```
apply時に対話方式で必要な情報をセットします
- `credential_path`
  - キー(json)のpath
  - 例: /Users/xxx/Downloads/jobcan-auto-xxx.json
- `cron`
  - Cloud Schedulerに登録するcron
  - 例: 0 9,12,13,18 * * 1,2,3,4,5（← 平日の9時、12時、13時、18時に実行）
- `jobcan_email`
  - ジョブカンにログインするときのメールアドレス
  - **この情報はSecret Managerに保存されます**
- `jobcan_password`
  - ジョブカンにログインするときのパスワード
  - **この情報はSecret Managerに保存されます**
- `project_id`
  - 作成したプロジェクトのID
  - 例: jobcan-auto
- `project_number`
  - 作成したプロジェクトのプロジェクト番号
  - 例: 123456789012
