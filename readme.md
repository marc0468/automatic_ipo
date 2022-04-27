# Automatic IPO

## はじめに

IPOを自動で申し込むツールです。
対応している証券会社は以下です。

* [SBI証券](https://www.sbisec.co.jp/ETGate)

## 動作環境

本ツールの動作にはGoogle Chromeがインストールされている必要があります。
またWindows11で開発、動作確認しているため他OSでの動作保証はありません。

## 使い方

`automatic_ipo.exe`と[config.json](config.json)を同じフォルダに置いて`automatic_ipo.exe`を実行してください。
`config.json`には証券会社のログインパスワードを記載します。

デフォルトでは`automatic_ipo.exe`と同じ階層にある`config.json`を開こうとします。
以下のように`--config <コンフィグファイルパス>`オプションをつけて実行すると、任意のコンフィグファイルを読み込ませることができます。

```cmd
automatic_ipo.exe --config sample.json
```

### config.jsonの記載内容

* sbi
  * is_disabled
    * 証券会社（SBI証券）のIPO自動申込みを有効（`true`）にするか無効（`false`）にするかを選択できます。
  * user_id
    * 証券会社（SBI証券）のユーザーネームを設定してください。
  * user_password
    * 証券会社（SBI証券）のパスワードを設定してください。
  * trading_password
    * 証券会社（SBI証券）の取引パスワードを設定してください。
* display
  * GUIを表示する（`true`）、表示しない（`false`）を選択できます。PowerShellなどで実行する場合は`false`に設定してください。
* is_headless
  * ツール実行時にブラウザ画面を表示する（`true`）、表示しない（`false`）を選択できます。
