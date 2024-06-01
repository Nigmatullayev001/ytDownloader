from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from pytube import YouTube
import os

API_TOKEN = '7157390158:AAEnzdOvxV_r32VkRrq8mhpnrUGfJzGeHNA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Menga YouTube video havolasini yuboring va men uni siz uchun yuklab beraman.")


@dp.message_handler(regexp='https://youtube.com/')
async def download_youtube_video(message: types.Message):
    url = message.text
    await message.reply("Videoni yuklab olmoqdaman, biroz kuting...")

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = stream.download()
        await message.reply_video(video=open(video_path, 'rb'))
        os.remove(video_path)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {str(e)}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
