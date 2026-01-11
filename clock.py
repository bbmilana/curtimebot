import asyncio
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
import os

# ===== Secrets =====
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

SIZE = 256
kst = pytz.timezone("Asia/Bishkek")
avatar_path = "avatar.png"

async def update_avatar():
    try:
        async with TelegramClient(StringSession(session), api_id, api_hash) as client:
            print("[INFO] TelegramClient запущен")

            # ===== Удаляем старые фото =====
            photos = await client.get_profile_photos('me')
            if photos.total > 0:
                await client(functions.photos.DeletePhotosRequest(id=photos))
            print(f"[INFO] Старые фото удалены: {photos.total}")

            # ===== Текущее кыргызстанское время =====
            now = datetime.now(kst)
            t = now.strftime("%H:%M")

            # ===== Создаем PNG =====
            img = Image.new("RGB", (SIZE, SIZE), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), t, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            draw.text(((SIZE - w) / 2, (SIZE - h) / 2), t, fill=(255, 255, 255), font=font)

            img.save(avatar_path)
            print(f"[INFO] PNG создан: {avatar_path}, размер: {img.size}, время: {t}")

            # ===== Загружаем новый аватар =====
            file = await client.upload_file(avatar_path)
            await client(functions.photos.UploadProfilePhotoRequest(file=file))
            print(f"[SUCCESS] Аватар обновлён: {datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC | {t} KST")

    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
    finally:
        print(f"[INFO] Workflow завершён: {datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")

asyncio.run(update_avatar())
