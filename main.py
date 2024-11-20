import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from parsing import get_post


load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Привет, Оливка, отправь ссылку с WB и я сделаю тебе пост. Тёма сыр, кстати")

@dp.message()
async def send_welcome(message: types.Message):
    post = get_post(message.text)
    description = "*{title}*\n\n*Цена:* {price}\n\n*Артикул:* {link}\n\n#Wildberries".format(title=post['product_title'], price=post['price'], link=post['link'])
    await bot.send_photo(chat_id=message.from_user.id, photo=post['image'], caption=description, parse_mode='Markdown')  

    
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())