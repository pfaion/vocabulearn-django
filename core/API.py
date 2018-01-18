from django.http import HttpResponse, JsonResponse

from .models import FlashCard, CardSet, Folder
import datetime

def card(request, card_id):
    card = FlashCard.objects.get(pk=card_id)
    if request.method == 'POST':
        front_first = request.POST['front_first'] == "true"
        marked = request.POST['marked'] == "true"
        card.update(request.POST['front'], request.POST['back'], front_first, marked)
        return HttpResponse('Saved.')
    elif request.method == 'GET':
        return JsonResponse(card.getDict())
        
def cards(request):
    if request.method == 'GET':
        data = [c.getDict() for c in FlashCard.objects.order_by('created_date')]
        return JsonResponse({"cards": data}) 

def new_card(request, set_id):
    if request.method == 'PUT':
        card = FlashCard()
        card.card_set = CardSet.objects.get(pk=set_id)
        card.save()
        return JsonResponse(card.getDict())

def delete_card(request, card_id):
    if request.method == 'DELETE':
        card = FlashCard.objects.get(pk=card_id)
        card.delete()
        return HttpResponse('Success')
        
def folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    if request.method == 'POST':
        folder.update(request.POST['name'])
        return HttpResponse('Saved.')

def folders(request):
    if request.method == 'GET':
        f = {'folders': [f.getDict() for f in Folder.objects.order_by('name')]}
        return JsonResponse(f)
        
def card_sets(request, folder_id=None):
    if folder_id is None:
        data = [c.getDict() for c in CardSet.objects.order_by('name')]
        return JsonResponse({"sets": data}) 
    folder = Folder.objects.get(pk=folder_id)
    if request.method == 'GET':
        data = [c.getDict() for c in CardSet.objects.order_by('name').filter(folder=folder.id)]
        return JsonResponse({"sets": data})
        

def new_folder(request):
    if request.method == 'PUT':
        folder = Folder()
        folder.save()
        return JsonResponse({'id': folder.id})
        
        
def card_set(request, set_id):
    card_set = CardSet.objects.get(pk=set_id)
    if request.method == 'POST':
        card_set.update(request.POST['name'])
        return HttpResponse('Saved.')
    elif request.method == 'GET':
        return JsonResponse(card_set.getDict())
        

def new_card_set(request, folder_id):
    if request.method == 'PUT':
        card_set = CardSet()
        card_set.folder = Folder.objects.get(pk=folder_id)
        card_set.save()
        return JsonResponse({'id': card_set.id})

def results(request, result):
    if request.method == 'GET':
        card_data, timestamp, marked_cards = result.split(";")
        if card_data != "":
            data = [pair.split(':') for pair in card_data.split(',')]
            for cardID, r in data:
                card = FlashCard.objects.get(pk=cardID)
                card.history = (r + card.history)[:16]
                card.last_trained_date = datetime.datetime.fromtimestamp(int(timestamp))
                card.save()
        if marked_cards != "":
            marked_ids = marked_cards.split(",")
            for cardID in marked_ids:
                card = FlashCard.objects.get(pk=cardID)
                card.marked = True
                card.save()
        return HttpResponse('Saved.')