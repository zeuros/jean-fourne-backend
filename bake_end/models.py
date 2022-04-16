import datetime

from django.db import models
from django.utils import timezone


class Coordinates(models.Model):
    url = models.CharField(max_length=600)
    lon = models.FloatField()
    lat = models.FloatField()

class Bakery(models.Model):
    name = models.CharField(max_length=600)
    coordinates = Coordinates()

class Client(models.Model):
    name = models.CharField(max_length=600)
    email = models.CharField(max_length=600)
    coordinates = Coordinates()
    birthDate = models.DateTimeField()

class Livreur(Client):
    pass

class Delivery(models.Model):
    client = Client()
    livreur = Livreur()
    coordinates = Coordinates()
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

#     def __str__(self):
#         return self.choice_text