# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import random



def clean_data(text):
    for ch in ['\\','`','«', '_','{','}','[',']','(',')','>','#','+','-','.','!','$','\'','»',',',':','"','”','xa0']:
        if ch in text:
            text = text.replace(ch,"")
    return text

def clean_dataNumbers(text):
    df=str(text)
    for ch in ['\\','`','«', '_','{','}','[',']','(',')','>','#','+','-','.','!','$','\'','»',',',':','"','”','xa0']:
        if ch in df:
            df = df.replace(ch,"")
    return int(df)


def remove_whitespace(value):
    return value.strip()



# def clean_scraped_data():
#     for j in range(0,60):
#         df['title'][j]=clean_data(df['title'][j])
#         df['details'][j]=clean_data(df['details'][j])
#         #df['date'][j]=clean_data(df['date'][j])
#     return df


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(
        input_processor= MapCompose(clean_data,remove_whitespace),
        output_processor= TakeFirst()
    )
    _id = scrapy.Field()
    id = scrapy.Field(
        input_processor=MapCompose(clean_dataNumbers),
        output_processor=TakeFirst()
    )
    details = scrapy.Field(
        input_processor=MapCompose(clean_data, remove_whitespace),
        output_processor=TakeFirst()
    )





