# from api.models import News
# from api.models import FakeNews
# from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
# from api.news import *



# class NewsDocumentSerializer(DocumentSerializer):
#     class Meta:
#         model = News
#         document = newsSearch

#         fields = ('title','content')

#         def get_location(self, obj):
#             try:
#                 return obj.location.to_dict()
#             except:
#                 return {}
                
