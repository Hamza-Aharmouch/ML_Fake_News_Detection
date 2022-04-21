from django.db import models

# Create your models here.
class News(models.Model):
    #id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=180)
    details = models.TextField()
    #date = models.CharField(max_length=80)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)


class FakeNews(models.Model):
    #id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=180)
    details = models.TextField()
    #date = models.CharField(max_length=80)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)


class DataText(models.Model):
    #id = models.AutoField(primary_key=True)
    #title = models.CharField(max_length=180)
    text = models.TextField()
    #date = models.CharField(max_length=80)
    
    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)




#class Book(models.Model):
#    title = models.CharField(max_length=100)
#    author = models.CharField(max_length=50)
#    year_published = models.CharField(max_length=10)
#    review = models.PositiveIntegerField()
    
#    def __str__(self):
#       return self.title