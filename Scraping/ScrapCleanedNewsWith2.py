import scrapy
import random
from Scraping_Project.items import NewsItem
from scrapy.loader import ItemLoader


class NewsSpider(scrapy.Spider):
    name = 'news5'

    start_urls = []
         #ICI on met l'URL du website
    def __init__(self):
        url = 'https://www.europe1.fr/dossiers/coronavirus/'
        for num in range(1, 100):
            self.start_urls.append(url + str(num))
        print(self.start_urls)



    #the parse methode
    def parse(self, response):
        for new in response.xpath("//div[@class='container extra-banner']"):
            choices = list(range(1500,9000))
            random.shuffle(choices)
            num = choices.pop()

            l= ItemLoader(item=NewsItem(),selector=new)
            l.add_value('id',num)
            l.add_xpath('title',"//header/h1//text()")
            l.add_xpath('details',"//div[@class='container']/article/section/strong//text()")

            # title = new.xpath("//header/h1//text()").getall()
            # detail = new.xpath("//div[@class='container']/article/section/strong//text()").getall()
            #date = new.xpath("//div[@class='row']/div/span[@class='publication']//text()").getall()

            yield l.load_item()
                # 'title': title,
                # 'details': detail,
                #'date': date,


            # on crée la variable pour prendre aussi les actualites dans les pages
        next_page_info = response.xpath("//div[@class='block block_lastcontent']/ul/li/div/div[@class='bloc_news']/a/@href").getall()
        for page_info in next_page_info:
            next_page_link_info = response.urljoin(page_info)
            yield scrapy.Request(url=next_page_link_info, callback=self.parse)




