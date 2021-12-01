# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или
# Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# - Наименование вакансии.
# - Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# - Ссылку на саму вакансию.
# - Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с
# помощью dataFrame через pandas. Сохраните в json либо csv.


import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

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

vacancies_list = []

pages = dom.find_all('span', {'class', 'pager-item-not-in-short-range'})
max_page = int(pages[-1].text)

for i in range(max_page):
    params = {'area': area,
              'text': search_name,
              'page': i - 1}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}
        body_vacancies = vacancy.find('a', {'class', 'bloko-link'}, {'data-qa',
                                                                     'vacancy-serp__vacancy-title'})
        name = body_vacancies.text
        link = body_vacancies.get('href')
        body_price = vacancy.find('div', {'class', "vacancy-serp-item__sidebar"})
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

        vacancies_list.append(vacancy_data)

pprint(vacancies_list)

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies_list, f, ensure_ascii=False)
