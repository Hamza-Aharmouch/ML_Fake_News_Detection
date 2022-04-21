#import datetime
from django_elasticsearch_dsl import (Document, fields, Index)
from api.models import News
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer
# from elasticsearch_dsl import (
#     Boolean,
#     Date,
#     Document,
#     InnerDoc,
#     Keyword,
#     Nested,
#     Text,
#     Integer,
# )

# class Comment(InnerDoc):

#     title = Text(fields={'raw': Keyword()})
#     details = Text(fields={'raw': Keyword()})
    
news_index = Index('news')
news_index.settings(
    number_of_shards=1,
    number_of_replicas=1
)
    

@registry.register_document
@news_index.doc_type
class newsSearch(Document):
    # title = Text(
    #     fields={'raw': Keyword()}
    # )
    # details = Text(
    #     fields={'raw': Keyword()}
    # )
    

    # class index:
    #     name = 'news'
    #     settings = {
    #         'number_of_shards': 1,
    #         'number_of_replicas': 1,
    #         #'blocks': {'read_only_allow_delete': None},
    #     }

    title = fields.TextField(
        fields={
            "raw": fields.TextField(analyzer='keyword')
            }
    )
   
    details = fields.TextField(
         fields={
            "raw": fields.TextField(analyzer='keyword')
            }
    )
    id = fields.IntegerField(attr="id")
    

    class Django:
        model = News
        #fields = ['title','details']