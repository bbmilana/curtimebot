from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
import os

# Берём значения из секретов
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

# Создаём картинку с текущим временем
now = datetime.now().strftime("%H:%M")
img = Image.new("RGB", (500, 500), "black")  # фон чёрный
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()
draw.text((200, 240), now, fill="white", font=font)

# Сохраняем картинку
img.save("avatar.jpg")

# Подключаемся к Telegram и меняем аватарку
with TelegramClient(StringSession(session), api_id, api_hash) as client:
    client.upload_profile_photo("avatar.jpg")
