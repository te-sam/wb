import re

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
    post['link'] = f"[{url.split('/')[4]}]({url})"
    post['image'] = soup.select_one('.photo-zoom__preview')['src']
    return post
    

