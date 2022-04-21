import random

import scrapy
from Scraping_Project.items import NewsItem
from scrapy.loader import ItemLoader


class NewsSpider(scrapy.Spider):
    name = 'news4'

    start_urls = [
        'https://www.lemonde.fr/coronavirus-2019-ncov/' #ICI on met l'URL du website
    ]

    #the parse methode
    def parse(self, response):

        for new in response.xpath("//div[@class='thread']"):
            choices = list(range(700,1500))
            random.shuffle(choices)
            num = choices.pop()

            l= ItemLoader(item=NewsItem(), selector=new)
            l.add_value('id', num)
            l.add_xpath('title',".//section/a/h3//text()")
            l.add_xpath('details',".//section/a/p//text()")

            #title = new.xpath(".//section/a/h3//text()").getall()
            #detail = new.xpath(".//section/a/p//text()").getall()
            #date = new.xpath(".//section/p/span[@class='meta__date']//text()").getall()

            yield l.load_item()
                # 'title': title,
                # 'details': detail,
                #'date': date,


        #on crée la variable pour prendre aussi les autres pages
        # next_page = response.xpath("//ul[@class='pagination']/li[@class='pager-next last']/a/@href").getall()
        # for page in next_page :
        #     if page is not None :
        #          next_page_link = response.urljoin(page)
        #          yield scrapy.Request(url=next_page_link, callback=self.parse)
