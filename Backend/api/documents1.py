# from django_elasticsearch_dsl import (Document, fields, Index)
# from api.models import News
# from api.models import FakeNews
# from django_elasticsearch_dsl.registries import registry
# from elasticsearch_dsl import analyzer


# News_index = Index('news')
# Fake_News_index = Index('fake_news')

# News_index.settings(
#     number_of_shards=1,
#     number_of_replicas=1
# )
# Fake_News_index.settings(
#     number_of_shards=1,
#     number_of_replicas=1
# )

# @registry.register_document
# @News_index.doc_type
# class NewsDocument(Document):
#     id = fields.IntegerField(attr="id")
#     title = fields.TextField(attr="title")
#     details = fields.TextField(attr="details")


#     class Django:
#         model = News