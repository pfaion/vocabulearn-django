from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import API

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('API/card/<int:card_id>/', API.card, name='card'),
    path('API/card/new/', API.new_card, name='card'),
    path('API/card/delete/<int:card_id>/', API.delete_card, name='card'),
]