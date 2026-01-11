import asyncio
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
import os

# ===== GitHub Secrets =====
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

SIZE = 256
kst = pytz.timezone("Asia/Bishkek")

# ===== Текущее время Кыргызстана =====
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

avatar_path = "avatar.png"
img.save(avatar_path)
print(f"PNG создан: {avatar_path}, размер: {img.size}, время: {t}")

# ===== Асинхронная функция с удалением старых фото =====
async def main():
    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        # 1️⃣ Получаем все фото профиля
        photos = await client.get_profile_photos('me')

        # 2️⃣ Удаляем все старые фото
        if photos.total > 0:
            await client(functions.photos.DeletePhotosRequest(id=photos))
            print(f"Удалено старых фото: {photos.total}")

        # 3️⃣ Загружаем новое фото
        try:
            file = await asyncio.wait_for(client.upload_file(avatar_path), timeout=20)
            result = await asyncio.wait_for(
                client(functions.photos.UploadProfilePhotoRequest(file=file)),
                timeout=20
            )
            print("Аватар обновлён")
        except asyncio.TimeoutError:
            print("Ошибка: загрузка или установка аватара заняла больше 20 секунд и была прервана")

        # 4️⃣ Лог времени запуска для проверки
        print(f"Workflow сработал: {datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")

asyncio.run(main())
