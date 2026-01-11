from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
import os

# ===== GitHub Secrets =====
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

SIZE = 512
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)

# ===== создаём PNG аватарку =====
img = Image.new("RGB", (SIZE, SIZE), "black")
draw = ImageDraw.Draw(img)
t = datetime.now().strftime("%H:%M")
bbox = draw.textbbox((0, 0), t, font=font)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]
draw.text(((SIZE - w) / 2, (SIZE - h) / 2), t, fill="white", font=font)
avatar_path = "avatar.png"
img.save(avatar_path)

# ===== загружаем в Telegram =====
with TelegramClient(StringSession(session), api_id, api_hash) as client:
    client.start()
    file = client.upload_file(avatar_path)
    client(functions.photos.UploadProfilePhotoRequest(file=file))
