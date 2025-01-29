import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboard import main_kb
from parsing import get_post


load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    give_link = State()
    give_title = State()
    give_links = State()


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(text="Привет, Оливка, отправь ссылку с WB и я сделаю тебе пост. Тёма сыр, кстати", reply_markup=main_kb(message.from_user.id))


# @dp.message("")
# async def post_from_message(message: types.Message):
#     post = get_post(message)
#     description = "*{title}*\n\n*Цена:* {price}\n*Артикул:* {link}\n\n#Wildberries".format(title=post['product_title'], price=post['price'], link=post['link'])
#     await bot.send_photo(chat_id=message.from_user.id, photo=post['image'], caption=description, parse_mode='Markdown') 


@dp.message(F.text == "Одинокий пост")
async def get_post_alone(message: types.Message, state: FSMContext):
    await message.answer("Отправь ссылку, красотка:")
    await state.set_state(Form.give_link)


@dp.message(Form.give_link)
async def make_post(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    print(data['link'])
    post = get_post(data['link'])
    description = "*{title}*\n\n*Цена:* {price}\n*Артикул:* {link}\n\n#Wildberries".format(title=post['product_title'], price=post['price'], link=post['link'])
    await bot.send_photo(chat_id=message.from_user.id, photo=post['image'], caption=description, parse_mode='Markdown') 
    await state.clear()


@dp.message(F.text == "Групповой пост")
async def get_title(message: types.Message, state: FSMContext):
    await message.answer("Отправь заголовок, детка")
    await state.set_state(Form.give_title)


@dp.message(Form.give_title)
async def get_group_from_posts(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Form.give_links)
    await message.answer("Отправь ссылки, крошка")


@dp.message(Form.give_links)
async def make_some_posts(message: types.Message, state: FSMContext):
    await state.update_data(links=message.text)
    data = await state.get_data()
    links = data['links'].split()
    posts_text = f"{data['title']}\n\n"
    image_links = []
    images = []

    print(data['title'])
    print(links)

    for n, link in enumerate(links):
        post = get_post(link)
        posts_text += f"{n+1}) {post['product_title']}\nЦена: {post['price']}\n*Артикул*: {post['link']}\n\n"
        image_links.append(post['image'])

    for image in image_links:
        print(image)
        images.append(InputMediaPhoto(media=image))
    
    # await bot.send_media_group(chat_id=message.from_user.id, media=images)
    await message.answer_media_group(images, caption=posts_text, text='Text123')


    # description = "*{title}*\n\n*Цена:* {price}\n\n*Артикул:* {link}\n\n#Wildberries".format(title=post['product_title'], price=post['price'], link=post['link'])
    # await bot.send_photo(chat_id=message.from_user.id, photo=post['image'], caption=description, parse_mode='Markdown') 
    await state.clear()




# from aiogram.utils.media_group import MediaGroupBuilder

# @router.message(UploadPostAd.photos)
# async def process_photos( message: Message, state: FSMContext):
#     # Process the photos here
#     if message.photo:
#         photo_ids = get_all_photo_ids(message)  # Get all photo IDs

#         media_group = MediaGroupBuilder(caption="Media group caption")
#         for photo in photo_ids:
#             media_group.add_photo(type="photo", media=photo)

#         await message.answer_media_group(media=media_group.build())
#         await state.clear()


    
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())