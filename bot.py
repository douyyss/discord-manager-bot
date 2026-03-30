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

TODO_CHANNEL = 1482700197833347112
CALENDAR_CHANNEL = 1482561786678087720
AUDIO_CHANNEL = 1482560346148569118


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if message.channel.id == TODO_CHANNEL:
        print("TODO追加")

    if message.channel.id == CALENDAR_CHANNEL:
        print("カレンダー追加")

    if message.channel.id == AUDIO_CHANNEL:
        print("音源保存")

    await bot.process_commands(message)

bot.run(os.environ['DISCORD_TOKEN'])
