import random

import scrapy
from Scraping_Project.items import NewsItem
from scrapy.loader import ItemLoader


class NewsSpider(scrapy.Spider):
    name = 'fakenews1'

    start_urls = [
        'https://www.legorafi.fr/?s=covid#' #ICI on met l'URL du website
    ]

    #the parse methode
    def parse(self, response):

        for new in response.xpath("//ul/li[@class='mvp-blog-story-wrap left relative infinite-post']"):
            choices = list(range(700,1500))
            random.shuffle(choices)
            num = choices.pop()

            l= ItemLoader(item=NewsItem(), selector=new)
            l.add_value('id', num)
            l.add_xpath('title',".//a/div/div[@class='mvp-blog-story-in']/div/h2//text()")
            l.add_xpath('details',".//a/div/div[@class='mvp-blog-story-in']/div/p//text()")

            yield l.load_item()


        #on crée la variable pour prendre aussi les autres pages
        next_page = response.xpath("//div[@class='mvp-inf-more-wrap left relative']/div/div/a/@href").getall()
        for page in next_page :
            if page is not None :
                 next_page_link = response.urljoin(page)
                 yield scrapy.Request(url=next_page_link, callback=self.parse)
