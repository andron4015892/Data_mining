
#  Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
#  конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
from pprint import pprint

# Пользователь для примера: Microsoft (https://github.com/microsoft)
response = requests.get("https://api.github.com/users/Microsoft/repos")
json_response = response.json()
pprint(json_response)

