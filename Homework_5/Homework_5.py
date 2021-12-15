from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import time
from pymongo import MongoClient


"""
Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает 
данные в БД. Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары.
"""


chrome_options = Options()
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

client = MongoClient('127.0.0.1', 27017)

db = client['M_Video']  # база данных

products = db.Products  # коллекция

driver.get('https://www.mvideo.ru/')
time.sleep(4)
# driver.implicitly_wait(10) - не помогает сдесь

# Scroll
driver.execute_script("window.scrollTo(0, 1500)")
driver.implicitly_wait(10)

button = driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']")
button.click()
# driver.implicitly_wait(10) - time.sleep всё же сдесь работает лучше
time.sleep(3)


# Отделение нужной части товаров
items = driver.find_element(By.XPATH, '//mvid-carousel[@class="carusel ng-star-inserted"]')

all_name_and_link = items.find_elements(By.XPATH, ".//div[@class='product-mini-card__name ng-star-inserted']") # "//div[@class='product-mini-card__name ng-star-inserted']"
all_price = items.find_elements(By.XPATH, ".//span[@class='price__main-value']")
# Сшивание all_name_and_link и all_prices
all_items = list(zip(all_name_and_link, all_price))

# product_list = []

# Формирование словорей
for one in all_items:
    product = {'name': one[0].text,
               'link': one[0].find_element(By.XPATH, ".//a").get_attribute('href'),
               'price': int(one[1].text.replace(' ', ''))}

    # Заносим в базу
    if len(list(products.find({'link': product['link']}))) > 0:
        print('Product already exists')
    else:
        products.insert_one(product)

    # print(price)
    # pprint(product)
    # product_list.append(product_dict)

# Закрытие драйвера
driver.quit()
