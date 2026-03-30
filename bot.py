import discord
import os
import datetime
import io
import json
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

TOKEN = os.getenv("DISCORD_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

TODO_CHANNEL = 1482700197833347112
CALENDAR_CHANNEL = 1482561786678087720
AUDIO_CHANNEL = 1482560346148569118

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

creds_dict = json.loads(GOOGLE_CREDENTIALS)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar"
]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

gc = gspread.authorize(credentials)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

drive_service = build("drive", "v3", credentials=credentials)
calendar_service = build("calendar", "v3", credentials=credentials)

@bot.event
async def on_ready():
    print("BOT STARTED:", bot.user)

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id == TODO_CHANNEL:
        text = message.content
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        sheet.append_row([text, "未完了", now])
        await message.add_reaction("✅")

    if message.channel.id == CALENDAR_CHANNEL:
        text = message.content
        event = {
            "summary": text,
            "start": {
                "dateTime": datetime.datetime.utcnow().isoformat(),
                "timeZone": "Asia/Tokyo"
            },
            "end": {
                "dateTime": (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat(),
                "timeZone": "Asia/Tokyo"
            }
        }
        calendar_service.events().insert(calendarId="primary", body=event).execute()
        await message.add_reaction("📅")

    if message.channel.id == AUDIO_CHANNEL:
        for attachment in message.attachments:
            data = await attachment.read()
            media = MediaIoBaseUpload(io.BytesIO(data), mimetype="audio/mpeg")
            drive_service.files().create(
                body={"name": attachment.filename},
                media_body=media
            ).execute()
            await message.add_reaction("💾")

    await bot.process_commands(message)

bot.run(TOKEN)
