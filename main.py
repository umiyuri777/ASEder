import discord
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime, time, timedelta, timezone
import requests
from bs4 import BeautifulSoup
from keep_alive import keep_alive
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

JST = timezone(timedelta(hours=+9), "JST")

times = [
	time(hour=20, minute=0, tzinfo=JST)
]

@tasks.loop(time=times)
async def send_message():
	now = datetime.now(JST)

	# 土曜日のみ実行
	if now.weekday() == 5:
		# AtCoderからコンテスト情報をスクレイピング
		response = requests.get('https://atcoder.jp/contests/')
		soup = BeautifulSoup(response.content, 'html.parser')
		contest_links = soup.find_all('a', href=True)

		atcoder_link = None
		for link in contest_links:
			href = link['href']

			# 最初に見つかった AtCoder Beginner Contest を抽出
			if '/contests/abc' in href:
				atcoder_link = f"https://atcoder.jp{href}"
				break

		if atcoder_link:
			channel_id=os.environ.get("DISCORD_CHANNEL_ID")
			channel = client.get_channel(int(channel_id))
			message = await channel.send(f'【テスト】次のAtCoder ABCコンテストはこちら: {atcoder_link}')
			await message.add_reaction("🔥")

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
