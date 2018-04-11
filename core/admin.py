from django.contrib import admin

from .models import Folder, CardSet, FlashCard, SetHistory

# Register your models here.
admin.site.register(Folder)
admin.site.register(CardSet)
admin.site.register(FlashCard)
admin.site.register(SetHistory)
