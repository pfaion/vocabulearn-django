from django.http import HttpResponse, JsonResponse

from .models import FlashCard, CardSet, Folder

def card(request, card_id):
    card = FlashCard.objects.get(pk=card_id)
    if request.method == 'POST':
        card.update(request.POST['front'], request.POST['back'])
        return HttpResponse('Saved.')
    elif request.method == 'GET':
        return JsonResponse(card.getDict())

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
        

def new_card_set(request, folder_id):
    if request.method == 'PUT':
        card_set = CardSet()
        card_set.folder = Folder.objects.get(pk=folder_id)
        card_set.save()
        return JsonResponse({'id': card_set.id})