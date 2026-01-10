from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

# создаём квадратное изображение 512x512
img = Image.new("RGB", (512, 512), "black")
draw = ImageDraw.Draw(img)

now = datetime.now().strftime("%H:%M")

# используем шрифт, который есть в Ubuntu (на GitHub Actions)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
except:
    font = ImageFont.load_default()

# текст по центру
w, h = draw.textsize(now, font=font)
draw.text(((512-w)/2, (512-h)/2), now, fill="white", font=font)

# сохраняем картинку
img.save("avatar.jpg")

# подключаемся к аккаунту и меняем аватар
with TelegramClient(StringSession(session), api_id, api_hash) as client:
    client.upload_profile_photo("avatar.jpg")
