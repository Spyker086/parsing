import sys
import time

from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
import datetime
from datetime import timedelta
import locale
# import time

client = MongoClient('127.0.0.1', 27017)
db = client['news_website']
news_db = db['news']

tz = int(str(datetime.datetime.now(datetime.timezone.utc).astimezone().timetz())[-5:-3])

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')

url = ['https://lenta.ru','https://news.mail.ru', 'https://yandex.ru/news']

try:
    n = int(input('Введите - 1 (Лента.ру), 2 (Маил.ру), 3 (Яндекс.ру): '))

except:
    print('!!!Некорректно введено значение!!!')
    sys.exit()

headers = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}

try:
    response = requests.get(url[n-1], headers=headers)
except:
    print('!!!Некорректно введено значение!!!')
    sys.exit()

mn_list = []
news_db.delete_many({})

if n == 1:
    dom_lenta = html.fromstring(response.text)
    main_news = dom_lenta.xpath("//section[@class='row b-top7-for-main js-top-seven']//h2 | //section[@class='row b-top7-for-main js-top-seven']//div[(@class='item')]")

    for i in main_news:
        mn_dict = {}
        source = 'lenta.ru'
        name = str(i.xpath(".//a/text()")[0]).replace(u'\xa0', u' ')
        if str(i.xpath(".//a/@href")).strip("[']")[1:5] != 'news':
            link = str(i.xpath(".//a/@href")).strip("[']")
            source = 'moslenta.ru'
        else:
            link = url[n-1] + str(i.xpath(".//a/@href")).strip("[']")
            source = 'lenta.ru'
        dt = datetime.datetime.strptime(str(i.xpath(".//time/@datetime")).strip("[']"),' %H:%M, %d %B %Y')
        mn_dict['source'] = source
        mn_dict['name'] = name
        mn_dict['link'] = link
        mn_dict['date'] = dt
        news_db.insert_one(mn_dict)

elif n == 2:
    dom_mail = html.fromstring(response.text)
    links = dom_mail.xpath("//div[contains(@class,'daynews__item')]//@href | //ul[contains(@class,'list_half')]/li[@class='list__item']//@href")

    for l in links:
        mn_dict = {}
        response_mail = requests.get(l, headers=headers)
        dom_mail_l = html.fromstring(response_mail.text)

        source = str(dom_mail_l.xpath("//a[@class='link color_gray breadcrumbs__link']/@href")).strip("[']")
        name = str(dom_mail_l.xpath("//h1[@class='hdr__inner']/text()")).strip("[']")
        link = l

        dt = datetime.datetime.strptime(str(dom_mail_l.xpath("//span[contains(@class,'js-ago')]/@datetime")).strip("[']")[:16], '%Y-%m-%dT%H:%M') + timedelta(hours=tz)
        mn_dict['source'] = source
        mn_dict['name'] = name
        mn_dict['link'] = link
        mn_dict['date'] = dt
        news_db.insert_one(mn_dict)

elif n == 3:
    dom_ya = html.fromstring(response.text)
    main_news = dom_ya.xpath("//div[contains(@class,'news-top-flexible-stories')]//article")

    for y in main_news:
        mn_dict = {}
        source = str(y.xpath(".//a[@class='mg-card__source-link']/text()")).strip("[']")
        name = str(y.xpath('.//h2//text()')).strip("[']").replace(u'\\xa0', u' ')
        link = str(y.xpath(".//a[@class='mg-card__link']/@href")).strip("[']")
        dt_con = str(datetime.datetime.now() - timedelta(hours=1))[:11] + str(y.xpath(".//span[@class='mg-card-source__time']/text()")).strip("[']")
        dt = datetime.datetime.strptime(dt_con, '%Y-%m-%d %H:%M')
        mn_dict['source'] = source
        mn_dict['name'] = name
        mn_dict['link'] = link
        mn_dict['date'] = dt
        news_db.insert_one(mn_dict)


for item in news_db.find():
    print(item)
