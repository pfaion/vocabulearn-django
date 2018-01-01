from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import API

urlpatterns = [
    path('', views.index, name='index'),
    path('set/<int:set_id>/', views.index, name='index'),
    path('login/', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('API/card/<int:card_id>/', API.card, name='card'),
    path('API/card/new/<int:set_id>/', API.new_card, name='card'),
    path('API/card/delete/<int:card_id>/', API.delete_card, name='card'),
    path('API/folder/<int:folder_id>/', API.folder, name='folder'),
    path('API/folder/new/', API.new_folder, name='folder'),
    path('API/folders/', API.folders, name='folders'),
    path('API/set/<int:set_id>/', API.card_set, name='card_set'),
    path('API/set/new/<int:folder_id>/', API.new_card_set, name='card_set'),
]