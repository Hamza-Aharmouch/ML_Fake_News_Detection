from django.shortcuts import render
#import requests
from api.models import *
from api.documents import *
from api.serializers import *
from django_elasticsearch_dsl_drf.viewsets import *
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
)





# class PublisherDocumentView(DocumentViewSet):
#     document = newsSearch
#     serializer_class = NewsDocumentSerializer

#     filter_backends = [
#         FilteringFilterBackend,
#         CompoundSearchFilterBackend
#     ]

#     search_fields = ('title','details')
#     multi_match_search_fields = ('title','details')
#     filter_fields = {
#         'title' : 'title',
#         'details' : 'details'
#     }
