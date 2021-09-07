import scrapy
from scrapy.http import HtmlResponse
from libparser.items import LibparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F/?available=1&wait=1&no=1&preorder=1&paperbooks=1']

    def parse(self, response: HtmlResponse):
        urls = response.xpath('//a[@class="product-title-link"]/@href').getall()
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        bk_url = response.url
        bk_name = response.xpath('//h1/text()').get()
        bk_author = response.xpath('//div[@class="authors"]/a[@data-event-label="author"]/text()').get()
        bk_price = response.xpath('//span[@class="buying-price-val-number"]/text()').get()
        bk_price_old = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        bk_price_dc = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        bk_rating = response.xpath('//div[@id="rate"]/text()').get()
        item = LibparserItem(url=bk_url,
                            name=bk_name,
                            author=bk_author,
                            price=bk_price,
                            price_old=bk_price_old,
                            price_dc=bk_price_dc,
                            rating=bk_rating)
        yield item

