import pymongo
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient
import json

"""
 1.Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
 которая будет добавлять только новые вакансии/продукты в вашу базу.
"""

client = MongoClient('127.0.0.1', 27017)

db = client['HeadHunter']  # база данных

vacancy = db.vacancy  # коллекция

# загрузить из json (файл из прошлого урока)
with open('vacancies.json', 'r', encoding='utf-8') as f:  # открываем файл на чтение
    vacancies = json.load(f)  # загружаем из файла данные в словарь vacancies

for vac in vacancies:
    link = vac['link']
    if len(list(vacancy.find({'link': link}))) > 0:
        print('Vacancy already exists')
    else:
        vacancy.insert_one(vac)

url = 'https://hh.ru'
area = 1
search_name = 'Data science'
page = 0

params = {'area': area,
          'text': search_name,
          'page': page}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})

pages = dom.find_all('span', {'class', 'pager-item-not-in-short-range'})
max_page = int(pages[-1].text)

for i in range(max_page):
    params = {'area': area,
              'text': search_name,
              'page': i - 1}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})

    for vac in vacancies:
        vacancy_data = {}
        body_vacancies = vac.find('a', {'class', 'bloko-link'}, {'data-qa',
                                                                 'vacancy-serp__vacancy-title'})
        name = body_vacancies.text
        link = body_vacancies.get('href')
        body_price = vac.find('div', {'class', "vacancy-serp-item__sidebar"})
        try:
            price = body_price.find('span').text.replace('\u202f', ' ')
            price = price.split()
            if price[0] == 'от':
                price_min = int(price[1] + price[2])
                price_max = None
                price_cur = price[-1]
            elif price[0] == 'до':
                price_min = None
                price_max = int(price[1] + price[2])
                price_cur = price[-1]
            else:
                price_min = int(price[0] + price[1])
                price_max = int(price[3] + price[4])
                price_cur = price[-1]
        except:
            price_min = None
            price_max = None
            price_cur = None

        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['source'] = url
        vacancy_data['price_min'] = price_min
        vacancy_data['price_max'] = price_max
        vacancy_data['price_cur'] = price_cur

        if len(list(vacancy.find({'link': link}))) > 0:
            print('Vacancy already exists')
        else:
            vacancy.insert_one(vacancy_data)

"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой 
больше введённой суммы (необходимо анализировать оба поля зарплаты). 
"""


def fand_money(money):
    for vacan in vacancy.find({'$or': [{'price_min': {'$gt': money}}, {'price_max': {'$gt': money}}]}):
        pprint(vacan)


salary = int(input("Введите желаемую ЗП: "))
fand_money(salary)
