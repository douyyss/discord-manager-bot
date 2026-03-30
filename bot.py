import discord
import os
import asyncio
import datetime
from discord.ext import commands, tasks
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # TODO BOT
    if message.channel.name == "todo":
        print("TODO追加")

    # 音源保存 BOT
    if message.channel.name == "音源保存":
        if message.attachments:
            print("音源保存")

    # カレンダー BOT
    if message.channel.name == "calendar":
        print("カレンダー追加")

    await bot.process_commands(message)

bot.run(os.environ['DISCORD_TOKEN'])
