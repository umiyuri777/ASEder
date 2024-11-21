import discord
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime, time, timedelta, timezone
import requests
from bs4 import BeautifulSoup
from keep_alive import keep_alive
import os
import random
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

JST = timezone(timedelta(hours=+9), "JST")

times = [
	time(hour=20, minute=0, tzinfo=JST)
]

# メッセージ候補リスト
messages = [
	"🗡️ 1時間後に **{contest_name}** が出現する！ [緊急クエスト受付](https://atcoder.jp{contest_url}) で準備を整えよう！",
	"🏹 ハンターよ、耳を傾けろ！**{contest_name}** が1時間後に姿を現す！ 急いで[狩猟準備](https://atcoder.jp{contest_url})だ！ 戦場に備えよ！",
	"🔥 緊急クエスト発生！**{contest_name}** の狩猟開始まであと1時間！ [ギルド情報](https://atcoder.jp{contest_url}) を確認せよ！",
	"⏰ 迫りくる時間！**{contest_name}** は1時間後に出現予定！ [集合場所](https://atcoder.jp{contest_url}) で待機せよ！",
	"⚔️ 狩猟隊、集結せよ！**{contest_name}** の討伐開始は1時間後だ！ [装備確認](https://atcoder.jp{contest_url}) を忘れるな！",
]

async def send_otsukaresama_message(channel):
	await asyncio.sleep(160 * 60)
	await channel.send("🎉 今日の狩猟お疲れ様でした！次回のクエストに向けて装備を整えましょう！")


@tasks.loop(time=times)
async def send_message():
	# AtCoderからコンテスト情報をスクレイピング
	response = requests.get('https://atcoder.jp/contests/')
	soup = BeautifulSoup(response.content, 'html.parser')
	table = soup.find(id="contest-table-upcoming")
	tbody = table.find('tbody')
	rows = tbody.find_all('tr')

	for row in rows:
		schedule_time = row.find('time').text.split(' ')[0]
		today = datetime.now(JST).strftime('%Y-%m-%d')

		# 本日の場合に実行
		if schedule_time == today:
			contest_links = row.find_all('a', href=True)

			for link in contest_links:
				contest_name = link.text.strip()
				contest_url = link['href']
				if '/contests/abc' in contest_url:
					# ランダムにメッセージを選択
					selected_message = random.choice(messages)
					formatted_message = selected_message.format(contest_name=contest_name, contest_url=contest_url)

					# チャンネルに送信
					channel_id = os.environ.get("DISCORD_CHANNEL_ID")
					channel = client.get_channel(int(channel_id))
					if channel:
						message = await channel.send(formatted_message)
						await message.add_reaction("🔥")
						asyncio.create_task(send_otsukaresama_message(channel))
						return

@client.event
async def on_ready():
	print(f'{client.user} 参上！')
	send_message.start()

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
try:
	client.run(TOKEN)
except:
	os.system("kill 1")
