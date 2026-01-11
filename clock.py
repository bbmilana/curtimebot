import asyncio
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

# ===== Создаем PNG аватарку без прозрачности =====
img = Image.new("RGB", (SIZE, SIZE), color=(0, 0, 0))  # черный фон
draw = ImageDraw.Draw(img)

t = datetime.now().strftime("%H:%M")
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
except:
    font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), t, font=font)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]
draw.text(((SIZE - w) / 2, (SIZE - h) / 2), t, fill=(255, 255, 255), font=font)

avatar_path = "avatar.png"
img.save(avatar_path)
print(f"PNG создан: {avatar_path}, размер: {img.size}")

# ===== Асинхронная функция для Telethon =====
async def main():
    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        file = await client.upload_file(avatar_path)
        result = await client(functions.photos.UploadProfilePhotoRequest(file=file))
        print("Результат загрузки в Telegram:")
        print(result)

# ===== Запуск =====
asyncio.run(main())
