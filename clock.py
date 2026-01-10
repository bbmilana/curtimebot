from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

# создаём квадратное изображение 512x512
img = Image.new("RGB", (512, 512), "black")
draw = ImageDraw.Draw(img)

now = datetime.now().strftime("%H:%M")

# используем шрифт Ubuntu
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
except:
    font = ImageFont.load_default()

# вычисляем ширину и высоту текста через textbbox
bbox = draw.textbbox((0, 0), now, font=font)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]

# рисуем текст по центру
draw.text(((512-w)/2, (512-h)/2), now, fill="white", font=font)

# сохраняем картинку
img.save("avatar.jpg")

# подключаемся к аккаунту и обновляем аватар
with TelegramClient(StringSession(session), api_id, api_hash) as client:
    client.start()
    file = client.upload_file("avatar.jpg")
    client(functions.photos.UploadProfilePhotoRequest(file=file))
