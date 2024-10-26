## ASEder
ASEder は、毎週土曜日の21時に開催される競技プログラミングイベント「AtCoder」のリンクを，スクレイピングによって自動的に指定したDiscordチャンネルに送信するDiscord Botです。

## 機能
- 毎週土曜日の21時にリマインド: ASEderのリンクを定期的に送信します。
- 自動通知: Botがリンクを指定されたチャンネルに送信するため、リマインドを忘れる心配がありません。

## 前提条件
- Python 3.11
- Discord Bot Token: DiscordでBotを稼働させるためのトークンが必要です。
- 必要なPythonライブラリ: discord.py などの依存ライブラリをインストールする必要があります。requirements.txtに集約されています。

## 利用方法
### このリポジトリをクローン

```
git clone https://github.com/shonsukee/ASEder.git
cd ASEder
```

### 依存関係をインストール
requirements.txt を使用して必要なパッケージをインストールします。

```
pip install -r requirements.txt
```

### Botの設定
.env ファイルに、以下の設定を行います：

DISCORD_TOKEN: Discord Botのトークン
DISCORD_CHANNEL_ID: 通知を送信するDiscordチャンネルのID
link: ASEderのリンク

## 使い方
### Botを起動する

以下のコマンドでBotを起動します：
```
python3 main.py
```

## 通知の送信

Botは毎週土曜日の21時になると、設定されたチャンネルにASEderのリンクを自動で送信します。

### カスタマイズ
通知するリンクの変更:  main.py 内の link の値を変更することで、送信するリンクをカスタマイズできます。
送信する曜日や時間の変更: main.py 内のスケジューリング部分を編集することで、通知を送信するタイミングを調整できます。
