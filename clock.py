from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
import os

# ===== берём данные из GitHub Secrets =====
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

# ===== создаём аватар =====
SIZE = 512
img = Image.new("RGB", (SIZE, SIZE), "black")
draw = ImageDraw.Draw(img)

now = datetime.now().strftime("%H:%M")

# шрифт (гарантированно есть в GitHub Actions)
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    150
)

# центрирование текста
bbox = draw.textbbox((0, 0), now, font=font)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]

draw.text(
    ((SIZE - w) / 2, (SIZE - h) / 2),
    now,
    fill="white",
    font=font
)

img.save("avatar.png")

# ===== обновляем аватар в Telegram =====
with TelegramClient(StringSession(session), api_id, api_hash) as client:
    client.start()

    file = client.upload_file("avatar.png")
    client(functions.photos.UploadProfilePhotoRequest(file=file))
