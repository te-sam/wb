import re
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep

def get_post(url_message: str):
    url = re.search(r'https://[^\s]+', url_message)[0]

    # Настройка опций для Chrome
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Включение безголового режима
    chrome_options.add_argument("--no-sandbox")  # Опционально, для некоторых систем
    chrome_options.add_argument("--disable-dev-shm-usage")  # Опционально, для устранения проблем с памятью
    chrome_options.add_argument("--disable-gpu")  # Отключение аппаратного ускорения
    chrome_options.add_argument("--enable-unsafe-swiftshader")

    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Открытие страницы
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-page__title")))
    sleep(1)

    post = {}
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    post['product_title'] = soup.find(class_='product-page__title').get_text(strip=True)
    post['price'] = soup.select_one('div.product-page__price-block.product-page__price-block--aside > div > div > div > p > span > ins').get_text(strip=True)
    post['price'] = post['price'][:-2] # обрезать Р
    post['link'] = f"[{url.split('/')[4]}]({url})"
    post['image'] = soup.select_one('.photo-zoom__preview')['src']
    return post
    

def fast_get_post(url: str):
    url = re.search(r'https://[^\s]+', url)[0]
    articul = url.split('/')[4]
    print(articul)
    response = requests.get(f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=123589415&spp=30&ab_testing=false&nm={articul}")

    if response.status_code == 200:
        post = {}
        n = len(articul)
    
        json_data = response.json()  # Получаем JSON-данные
        sizes = json_data['data']['products'][0]['sizes']

        #Название
        post['product_title'] = json_data['data']['products'][0]['name']

        #Цена
        for i in range(len(sizes)):
            if 'price' in sizes[i].keys():
                post['price'] = round(json_data['data']['products'][0]['sizes'][i]['price']['product'] / 100)

        #Ссылка
        post['link'] = f"[{articul}]({url})"

        #Картинка
        # post['image'] = None   
        # for i in range(n, 6, -1):
        #     for count in range(1, 23):  # на еденицу есть косяки
        #         if count < 10:
        #             image = f"https://basket-0{count}.wbbasket.ru/vol{articul[:i-5]}/part{articul[:i-3]}/{articul[:i]}/images/big/1.webp"
        #         else:
        #             image = f"https://basket-{count}.wbbasket.ru/vol{articul[:i-5]}/part{articul[:i-3]}/{articul[:i]}/images/big/1.webp"

        #         response = requests.get(image)
        #         if response.status_code == 200:
        #             card_url = f'{image[:-18]}/info/ru/card.json'
        #             response = requests.get(card_url)
                    
                    
        #             json_data = response.json() 
        #             get_articul = str(json_data['nm_id'])

        #             print(f'card url = {card_url}')
        #             print(f'Артикул: {json_data["nm_id"]}')
        #             print(f'Наш артикул: {articul}\n')

        #             if get_articul == articul:
        #                 post['image'] = image
        #                 break
        #         count += 1
        #     if post['image']:
        #         break

        post['image'] = None   
        for i in range(n, 6, -1):
            for count in range(1, 23):  # на еденицу есть косяки
                if count < 10:
                    card = f"https://basket-0{count}.wbbasket.ru/vol{articul[:i-5]}/part{articul[:i-3]}/{articul[:i]}/info/ru/card.json"
                else:
                    card = f"https://basket-{count}.wbbasket.ru/vol{articul[:i-5]}/part{articul[:i-3]}/{articul[:i]}/info/ru/card.json"

                response = requests.get(card)
                if response.status_code == 200:
                    json_data = response.json() 
                    get_articul = str(json_data['nm_id'])

                    print(f'card url = {card}')
                    print(f'Артикул: {json_data["nm_id"]}')
                    print(f'Наш артикул: {articul}\n')

                    if get_articul == articul:
                        post['image'] = f'{card[:-18]}/images/big/1.webp'
                        print(post['image'])
                        break
                count += 1

            if post['image']:
                break
            
        if not post['image']:
            print(f'Не найдена картинка(')
            return None

        return post
    else:
        print(f"Запрос не прошел: {response.status_code}")
    return None

