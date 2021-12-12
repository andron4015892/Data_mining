import pymongo
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient
import json
from pymongo.errors import *

"""
 1.Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
 которая будет добавлять только новые вакансии/продукты в вашу базу.
"""

client = MongoClient('127.0.0.1', 27017)

db = client['HeadHunter']  # база данных

vacancy = db.vacancy  # коллекция

# vacancy.delete_many({})
#
# test = {
#     "name": "Data Scie",
#     "link": "https://hh.ru/vacancy/11111",
#     "source": "https://hh.ru",
#     "price_min": 1,
#     "price_max": 6,
#     "price_cur": 'null'
# }
#
# vacancy.insert_one(test)

# Делаею поле link уникальным(что поможет избежать дублей)
vacancy.create_index([('link', pymongo.TEXT)], name='unique link', unique=True)

# загрузить из json (файл из прошлого урока)
with open('vacancies.json', 'r', encoding='utf-8') as f:  # открываем файл на чтение
    vacancies = json.load(f)  # загружаем из файла данные в словарь vacancies_list

# pprint(vacancies_list)

# Добовляем имеющиеся вакансии из прошлого урока
for vac in vacancies:
    try:
        vacancy.insert_one(vac)
    except DuplicateKeyError as error:
        print(error)

"""
Это ошибка не дающая сделть link уникальным
E11000 duplicate key error collection: HeadHunter.vacancy index: unique link dup key: { _fts: "20scienc", _ftsx: 0.5555555555555556 }, full error: {'index': 0, 'code': 11000, 'keyPattern': {'_fts': 'text', '_ftsx': 1}, 'keyValue': {'_fts': '20scienc', '_ftsx': 0.5555555555555556}, 'errmsg': 'E11000 duplicate key error collection: HeadHunter.vacancy index: unique link dup key: { _fts: "20scienc", _ftsx: 0.5555555555555556 }'}
"""

"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой 
больше введённой суммы (необходимо анализировать оба поля зарплаты). 
"""

# money = int(input("Введите желаемую ЗП: "))
#
# for doc in vacancy.find({'$or': [{'price_min': {'$gt': money}}, {'price_max': {'$gt': money}}]}):
#    pprint(doc)
