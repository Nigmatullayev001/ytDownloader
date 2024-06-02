# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.dispatcher.filters import Text
# from aiogram.types import ParseMode
# from aiogram.utils import executor
# from pytube import YouTube
# import os
#
# API_TOKEN = '7157390158:AAEnzdOvxV_r32VkRrq8mhpnrUGfJzGeHNA'
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
# dp.middleware.setup(LoggingMiddleware())
#
#
# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: types.Message):
#     await message.reply("Salom! Menga YouTube video havolasini yuboring va men uni siz uchun yuklab beraman.")
#
#
# @dp.message_handler(Text(startswith='https://youtu'))
# async def download_youtube_video(message: types.Message):
#     url = message.text
#     await message.reply("Videoni yuklab olmoqdaman, biroz kuting...")
#
#     try:
#         yt = YouTube(url)
#         stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
#         video_path = stream.download()
#         video = open(video_path, 'rb')
#         await message.reply_video(video=video)
#         os.remove(video_path)
#     except Exception as e:
#         await message.reply(f"Xatolik yuz berdi: {str(e)}")
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp)


import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
# from aiohttp_socks import ProxyConnector
from pytube import YouTube

API_TOKEN = '7157390158:AAEnzdOvxV_r32VkRrq8mhpnrUGfJzGeHNA'

lang = {"lang": 'en'}
# Xabarlarni uch tilda sozlash
messages = {
    'start': {
        'en': "Hello! Send me a YouTube video link and I will download it for you.",
        'uz': "Salom! Menga YouTube video havolasini yuboring va men uni siz uchun yuklab beraman.",
        'ru': "Привет! Отправьте мне ссылку на видео с YouTube, и я скачаю его для вас."
    },
    'downloading': {
        'en': "Downloading the video, please wait...",
        'uz': "Videoni yuklab olmoqdaman, biroz kuting...",
        'ru': "Скачиваю видео, пожалуйста подождите..."
    },
    'error': {
        'en': "An error occurred: ",
        'uz': "Xatolik yuz berdi: ",
        'ru': "Произошла ошибка: "
    }
}


def get_message(message_key, lang_code):
    return messages[message_key].get(lang_code, messages[message_key]['en'])


async def main():
    # connector = ProxyConnector.from_url(PROXY_URL)
    # async with ClientSession(connector=connector) as session:
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())

    # Til tanlash tugmachalarini yuklash
    from keyboard import keylang

    @dp.message_handler(commands=['start', 'settings'])
    async def send_welcome(message: types.Message):
        await message.reply("Please select your language:", reply_markup=keylang())

    @dp.message_handler(lambda message: message.text in ['English 🇬🇧', 'Oʻzbek 🇺🇿', 'Русский 🇷🇺'])
    async def set_language(message: types.Message):
        if message.text == 'English 🇬🇧':
            lang_code = 'en'
        elif message.text == 'Oʻzbek 🇺🇿':
            lang_code = 'uz'
        else:
            lang_code = 'ru'
        await message.reply(get_message('start', lang_code), reply_markup=types.ReplyKeyboardRemove())
        lang['lang'] = lang_code

    @dp.message_handler(Text(startswith='https://youtu'))
    async def download_youtube_video(message: types.Message):
        await message.reply(get_message('downloading', lang['lang']))

        try:
            url = message.text
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            video_path = stream.download()
            await message.reply_video(video=open(video_path, 'rb'))
            os.remove(video_path)
        except Exception as e:
            await message.reply(get_message('error', lang['lang']) + str(e))

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
