import scrapy
from scrapy.http import HtmlResponse
from libparser.items import LibparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi/?section_id=1159']
    num_p = 1

    def parse(self, response: HtmlResponse):
        urls = response.xpath('//div[@class="product-list__item"]//a[contains(@class,"image-link")]/@href').getall()
        n = len(urls)
        url_short = 'https://book24.ru/novie-knigi/'
        if n == 30:
            self.num_p += 1
            next_page = f'{url_short}page-{self.num_p}/?section_id=1159'
        else:
            next_page = False
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.book24_parse)


    def book24_parse(self, response: HtmlResponse):
        bk_url = response.url
        bk_name = response.xpath('//h1/text()').get()
        bk_author = response.xpath('//span[contains(text(),"Автор")]/../..//a/text()').get()
        bk_price = response.xpath('//span[@class="app-price product-sidebar-price__price"]/meta[@itemprop="price"]/@content').get()
        bk_price_old = None
        bk_price_dc = None
        bk_rating = response.xpath('//span[@class="rating-widget__main-text"]/text()').get()
        item = LibparserItem(url=bk_url,
                            name=bk_name,
                            author=bk_author,
                            price=bk_price,
                            price_old=bk_price_old,
                            price_dc=bk_price_dc,
                            rating=bk_rating)
        yield item