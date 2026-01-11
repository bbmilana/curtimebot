from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
import os

# ===== берём данные из GitHub Secrets =====
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

SIZE = 512
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)

# ===== создаём GIF с 60 кадрами (каждая минута) =====
frames = []
for i in range(60):
    img = Image.new("RGB", (SIZE, SIZE), "black")
    draw = ImageDraw.Draw(img)
    t = (datetime.now() + timedelta(minutes=i)).strftime("%H:%M")
    bbox = draw.textbbox((0, 0), t, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((SIZE - w) / 2, (SIZE - h) / 2), t, fill="white", font=font)
    frames.append(img)

frames[0].save(
    "avatar.gif",
    save_all=True,
    append_images=frames[1:],
    duration=60000,  # 60000ms = 1 минута на кадр
    loop=0
)

# ===== загружаем GIF в Telegram =====
with TelegramClient(StringSession(session), api_id, api_hash) as client:
    client.start()
    file = client.upload_file("avatar.gif")
    client(functions.photos.UploadProfilePhotoRequest(file=file))
