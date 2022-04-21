from django.contrib import admin
from .models import News, FakeNews

# Register your models here.
admin.site.register(News)
admin.site.register(FakeNews)
#admin.site.register(Book)