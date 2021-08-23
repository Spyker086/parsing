
import requests
import json
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
import sys
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017,  username='Admin', password='3%@Artur')
db = client['roscontrol']

products_db = db['products_db']

choose_clear = int(input('Очистить БД перед запуском? [1] - Да, [0] - Нет: '))

if choose_clear not in [0, 1]:
    print('!!!Некорректный ввод!!!')
    sys.exit()
elif choose_clear == 1:
    products_db.delete_many({})

url = 'https://roscontrol.com'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.3'}
find = input('Введите наименование продукта для поиска: ')
page = 1
try:
    page_count = int(input('Введите кол-во страниц для обработки: '))
except:
    print('!!!Введите число страниц!!!')
    sys.exit()

product_lst = []

while page <= page_count:
    params = {'keyword':find.encode(encoding='utf-8'), 'page': page}
    responce = requests.get(url + '/testlab/search', params=params, headers=headers)
    soup = bs(responce.text, 'html.parser')
    products = soup.find_all('div', attrs={'class':'wrap-product-catalog__item'})

    if len(products) == 0:
        print('!!!По данному запросу продукты не найдены!!!')
        sys.exit()

    elif len(products) <= 12:
        rating_list_p = []
        for product in products:
            product_data = {}
            name = product.find('div', attrs={'class':'product__item-link'}).text
            rate = int(product.find('div', attrs={'class':'rate'}).text)

            for i in range(len(product.find_all('div', attrs={'class':'right'}))):
                rating_list_p.append(int(product.find_all('div', attrs={'class':'right'})[i].text))

            rating = rating_list_p
            rating_list_p = []

            link = url + product.find('a')['href']

            product_data['name'] = name
            product_data['rate'] = rate
            product_data['rating'] = rating
            product_data['link'] = link
            # print(product_data)

            if products_db.count_documents({'link': link}) >= 1:
                print(f'{name} - уже в БД!!! Документ не внесен в БД!!!')
            else:
                products_db.insert_one(product_data)

    page += 1
    if len(products) < 12:
        page = page_count + 1

for i in products_db.find({}):
    print(i)

