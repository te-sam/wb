import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from aiogram.types import InputMediaPhoto

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboard import main_kb, hastags_kb, another_post_kb, cancel_kb
from parsing import get_post, fast_get_post



load_dotenv()
if os.getenv("MODE") == "TEST":
    bot = Bot(token=os.getenv("TEST_API_TOKEN"))
    print(os.getenv("MODE"))
else:
    bot = Bot(token=os.getenv("API_TOKEN"))
    print(os.getenv("MODE"))
storage = MemoryStorage()
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    give_link = State()
    give_title = State()
    give_hashtag = State()
    give_links = State()


async def print_post(link: str, message: types.Message):
    post = fast_get_post(link)

    if post is None:
        await message.answer("Нужно чуть-чуть подождать(")
        post = get_post(link)

    if 'product_title' in post.keys():
        await message.answer(f'Товара "{post["product_title"]}" нет в наличии')
        return None

    print(post)
    description = "*{title}*\n\n*Цена:* {price} ₽\n*Артикул:* {link}\n\n#Wildberries".format(title=post['product_title'], price=post['price'], link=post['link'])
    await bot.send_photo(chat_id=message.from_user.id, photo=post['image'], caption=description, parse_mode='Markdown', reply_markup=main_kb(message.from_user.id)) 


@dp.message(StateFilter("*"), F.text == "Отмена")  # "*" ловит любое состояние
async def quit_in_state(message: types.Message, state: FSMContext):
    print("Обработчик quit вызван (в любом состоянии)")
    await state.clear()
    print("Состояние после очистки:", await state.get_state())  # Должно быть None
    await message.answer('Выбирай, сударыня', reply_markup=main_kb(message.from_user.id))


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(text="Привет, Оливка, отправь ссылку с WB и я сделаю тебе пост. Тёма сыр, кстати", reply_markup=main_kb(message.from_user.id))


@dp.message(F.text == "Одинокий пост")
async def get_post_alone(message: types.Message, state: FSMContext):
    await message.answer("Отправь ссылку, красотка:", reply_markup=cancel_kb(message.from_user.id))
    await state.set_state(Form.give_link)


@dp.message(Form.give_link)
async def make_post(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    print(data['link'])
    await print_post(data['link'], message)
    await state.clear()


@dp.message(F.text == "Групповой пост (целиком)")
@dp.message(F.text == "Групповой пост (только артикулы)")
async def get_title(message: types.Message, state: FSMContext):
    await state.update_data(type_group=message.text)
    await message.answer("Отправь заголовок, детка", reply_markup=cancel_kb(message.from_user.id))
    await state.set_state(Form.give_title)


@dp.message(Form.give_title)
async def get_hashtag(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Form.give_hashtag)
    await message.answer("Отправь хэштэг, если без хэштэга, отправь пустое сообщение", reply_markup=hastags_kb(message.from_user.id))


@dp.message(Form.give_hashtag)
async def get_group_from_posts(message: types.Message, state: FSMContext):
    await state.update_data(hashtag=message.text)
    await state.set_state(Form.give_links)
    await message.answer("Отправь ссылки, крошка", reply_markup=cancel_kb(message.from_user.id))


@dp.message(Form.give_links)
async def make_some_posts(message: types.Message, state: FSMContext):
    await state.update_data(links=message.text)
    data = await state.get_data()
    links = data['links'].split()

    if len(links) > 10:
        await message.answer("Будут обработаны только первые 10 ссылок", reply_markup=cancel_kb(message.from_user.id))
        links = links[:10]

    posts_text = f"*{data['title']}*\n\n"
    image_links = []
    images = []

    if data['hashtag'] == "Без хэштега":
        hashtag = ""
    else:
        hashtag = data['hashtag'].replace("_", "\_")

    print(data['title'])
    print(links)

    i = 1  # переменная для начала нумерации списка товаров
    for n, link in enumerate(links):
       
        post = fast_get_post(link)

        if post is None:
            post = get_post(link)

        if 'price' not in post.keys():
            await message.answer(f'Товара "{post["product_title"]}" нет в наличии')
            i -= 1
            continue

        if data['type_group'] == "Групповой пост (целиком)":
            posts_text += f"*{n+i}) Цена:* {post['price']} ₽\n*Артикул*: {post['link']}\n"
        else:
            posts_text += f"*{n+i}) Артикул*: {post['link']}\n"
        image_links.append(post['image'])

    for image in image_links:
        print(image)
        images.append(InputMediaPhoto(media=image))
    
    if images:
        images[0].caption = posts_text + "\n#Wildberries\n" + hashtag
        images[0].parse_mode = 'Markdown'

    await message.answer_media_group(media=images)
    await message.answer("Ещё постик?",reply_markup=main_kb(message.from_user.id))
    await state.clear()


@dp.message(F.text == 'Сделать ещё пост😊')
async def redirect_main(message: types.Message, state: FSMContext):
    await message.answer("Выбирайте, сударыня", reply_markup=main_kb(message.from_user.id))



@dp.message()
async def echo(message: types.Message):
    await print_post(message.text, message)

    
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())