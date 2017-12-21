from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Folder, CardSet, FlashCard

# Create your views here.
@login_required
def index(request, set_id=None):
    
    directory = {
        folder: list(CardSet.objects.order_by('name').filter(folder=folder.id))
        for folder in Folder.objects.order_by('name')
    }
    print(directory)
    
    
    
    
    flash_cards = [f.getDict() for f in FlashCard.objects.order_by('created_date')]
        
    context = {
        'flash_cards': flash_cards,
        'directory': directory
    }
    return render(request, 'core/index.html', context)

def login(request):
    if request.method == 'GET':
        return render(request, 'core/login.html', {})
        
    elif request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('/')
        else:
            redirect('/login/')
        