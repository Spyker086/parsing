import requests
import json
from pprint import pprint

url = 'https://pressmon.com/api'
word = input('Введите фразу: ')
API_key = 'lAXWclSU3k'

resource = requests.get(f'{url}?q={word}&key={API_key}&l=ru&size=5').json()
result = []
if resource.get('hits') == None:
    result.append('Нет упоминаний')
else:
    for i in range(len(resource.get('hits'))):
        source = resource.get('hits')[i].get('source')
        text = resource.get('hits')[i].get('body')
        year = resource.get('hits')[i].get('pub_year')
        result.append(f'Издание- {source}; Упоминание- {text}; год публикации- {year}')

with open('task2.json', 'w') as f:
    json.dump(result, f, ensure_ascii = False, indent = 1)

pprint(result)