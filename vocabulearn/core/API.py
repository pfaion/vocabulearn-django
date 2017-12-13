from django.http import HttpResponse, JsonResponse

from .models import FlashCard

def card(request, card_id):
    card = FlashCard.objects.get(pk=card_id)
    if request.method == 'POST':
        card.update(request.POST['front'], request.POST['back'])
        return HttpResponse('Saved.')
    elif request.method == 'GET':
        return JsonResponse(card.getDict())

def new_card(request):
    if request.method == 'PUT':
        card = FlashCard()
        card.save()
        return JsonResponse(card.getDict())