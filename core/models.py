from django.db import models

from django.forms.models import model_to_dict
from django.utils.text import Truncator
from django.utils import timezone

from easydict import EasyDict

# Create your models here.

class FlashCard(models.Model):
    front = models.CharField(max_length=2000)
    back = models.CharField(max_length=2000)
    created_date = models.DateTimeField('date created', default=timezone.now)
    
    trunc_length = 20
    
    def __str__(self):
        return "{} - {}".format(self.front, self.back)

    def getDict(self):
        data = model_to_dict(self)
        data['front_short'] = Truncator(data['front']).chars(self.trunc_length)
        data['back_short'] = Truncator(data['back']).chars(self.trunc_length)
        return EasyDict(data)
    
    def update(self, front, back):
        self.front = front
        self.back = back
        self.save()