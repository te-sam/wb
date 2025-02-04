import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def get_price_block(price: str, font_size=50, block_width: int = 170, backround_path='images/price_background.png', font_path='fonts/arial.ttf', text_color='#1c0920'):
    # Открываем изображение
    image = Image.open(backround_path).convert("RGBA")
    print(f'Размеры до: {image.size}')
    image = image.resize((block_width, image.size[1]))
    print(f'Размеры после: {image.size}')
    
    # Создаем объект для рисования
    draw = ImageDraw.Draw(image)

    # Загружаем шрифт
    font = ImageFont.truetype(font_path, font_size)

    # Получаем размеры текста с помощью textbbox()
    text_bbox = draw.textbbox((0, 0), price, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Вычисляем позицию для центрирования текста
    image_width, image_height = image.size
    position = ((image_width - text_width) // 1.7, (image_height - text_height) // 2)

    # Накладываем текст на изображение
    draw.text(position, price, font=font, fill=text_color)  # Цвет текста можно изменить

    return image


def get_images_with_price(photo_url: str, price: int, position=(500, 100)):
    # Загружаем фоновое изображение по URL
    response = requests.get(photo_url)
    background = Image.open(BytesIO(response.content)).convert("RGBA")
    
    # Создаем новое изображение с альфа-каналом
    combined = Image.new("RGBA", background.size)

    # Накладываем фоновое изображение
    combined.paste(background, (0, 0))

    price_str = f'{price} Р'

    if price >= 10000:
        price_block = get_price_block(price_str, font_size=38)
    if 1000 <= price < 10000:
        price_block = get_price_block(price_str, font_size=38, block_width=140)
    if 100 <= price < 1000:
        price_block = get_price_block(price_str, font_size=38, block_width=120)
    if price < 100:
        price_block = get_price_block(price_str, font_size=38, block_width=100)


    # Накладываем второе изображение (текст) в указанной позиции
    combined.paste(price_block, position, price_block)

    combined.save('images/result.png')

    byte_stream = BytesIO()
    combined.save(byte_stream, format='PNG')  # Сохраните в нужном формате
    byte_stream.seek(0)

    return byte_stream


background_image_url = 'https://basket-18.wbbasket.ru/vol2917/part291753/291753387/images/big/4.webp'  # URL к фоновому изображению
price = 14
get_images_with_price(background_image_url, price, position=(650, 100))
