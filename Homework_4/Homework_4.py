from lxml import html
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
from pprint import pprint


"""
1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru,
yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
    * название источника;
    * наименование новости;
    * ссылку на новость;
    * дата публикации.
2. Сложить собранные новости в БД.
Минимум один сайт, максимум - все три.
"""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get('https://yandex.by/news/', headers=headers)

dom = html.fromstring(response.text)

news = []
all_page = dom.xpath("//article[contains(@class, 'mg-card mg-card_flexible')] | "
                     "//article[contains(@class,'mg-card mg-card_type_image mg-card_stretching "
                     "mg-card_flexible-double mg-grid__item')]")

client = MongoClient('127.0.0.1', 27017)

db = client['News']  # база данных

yandex = db.yandex  # коллекция

today = datetime.today().strftime('%d-%m-%Y')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%d-%m-%Y')

for one_news in all_page:

    piece_of_news = {}

    source = one_news.xpath(".//a[@class='mg-card__source-link']/text()")[0]
    news_title = one_news.xpath(".//h2[@class='mg-card__title']/text()")[0].replace('\xa0', ' ')
    link = one_news.xpath(".//h2[@class='mg-card__title']/../@href")[0]
    date_of_publication = one_news.xpath(".//span[@class='mg-card-source__time']/text()")[0]

    piece_of_news['source'] = source
    piece_of_news['news_title'] = news_title
    piece_of_news['link'] = link
    date_of_publication = date_of_publication.split()
    if date_of_publication[0] == 'вчера':
        piece_of_news['date_of_publication'] = date_of_publication[2] + ' ' + yesterday
    else:
        piece_of_news['date_of_publication'] = date_of_publication[0] + ' ' + today

    if len(list(yandex.find({'link': link}))) > 0:
        print('News already exists')
    else:
        yandex.insert_one(piece_of_news)
    #news.append(piece_of_news)

#pprint(news)