from django.db import models

from django.forms.models import model_to_dict
from django.utils.text import Truncator
from django.utils import timezone

from easydict import EasyDict

# Create your models here.




class Folder(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
    def update(self, name):
        self.name = name
        self.save()
    
    def getDict(self):
        data = model_to_dict(self)
        return EasyDict(data)
        

class CardSet(models.Model):
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def update(self, name):
        self.name = name
        self.save()
        
    def getDict(self):
        data = model_to_dict(self)
        return EasyDict(data)
        

class FlashCard(models.Model):
    front = models.CharField(max_length=2000)
    back = models.CharField(max_length=2000)
    created_date = models.DateTimeField('date created', default=timezone.now)
    card_set = models.ForeignKey(CardSet, on_delete=models.CASCADE)
    
    trunc_length = 20
    
    def __str__(self):
        return "{} - {}".format(self.front, self.back)

    def getDict(self):
        data = model_to_dict(self)
        return EasyDict(data)
    
    def update(self, front, back):
        self.front = front
        self.back = back
        self.save()