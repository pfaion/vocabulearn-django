from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Folder, CardSet, FlashCard

# Create your views here.
@login_required
def index(request, set_id=None):
    
    if set_id is None:
        for folder in Folder.objects.order_by('name'):
            sets = CardSet.objects.filter(folder=folder)
            if len(sets) > 0:
                set_id = sets.order_by('name').first().id
                break
    
    
    directory = {
        folder: list(CardSet.objects.order_by('name').filter(folder=folder.id))
        for folder in Folder.objects.order_by('name')
    }
    
    current_set = CardSet.objects.get(pk=set_id)
    flash_cards = FlashCard.objects.filter(card_set=current_set).order_by('created_date')
    if len(flash_cards) == 0:
        card = FlashCard()
        card.card_set = current_set
        card.save()
    flash_cards = FlashCard.objects.filter(card_set=current_set).order_by('created_date')
    flash_cards = [f.getDict() for f in flash_cards]
        
    context = {
        'flash_cards': flash_cards,
        'directory': directory,
        'set_id': set_id,
    }
    return render(request, 'core/index.html', context)


@login_required
def marked(request):
    
    directory = {
        folder: list(CardSet.objects.order_by('name').filter(folder=folder.id))
        for folder in Folder.objects.order_by('name')
    }
    
    flash_cards = FlashCard.objects.filter(marked=True).order_by('created_date')
    if len(flash_cards) == 0:
        return redirect("/")
    
    flash_cards = [f.getDict() for f in flash_cards]
        
    context = {
        'flash_cards': flash_cards,
        'directory': directory,
        'set_id': -1,
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
        