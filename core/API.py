from django.http import HttpResponse, JsonResponse

from .models import FlashCard, CardSet

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