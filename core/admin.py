from django.contrib import admin

from .models import Folder, CardSet, FlashCard

# Register your models here.
admin.site.register(Folder)
admin.site.register(CardSet)
admin.site.register(FlashCard)