from django.http import HttpResponse, JsonResponse

from .models import FlashCard, CardSet, Folder, SetHistory
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import datetime
import time
import io

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
        
def make_snapshot(set_id):
    card_set = CardSet.objects.get(pk=set_id)
    h = SetHistory.objects.filter(card_set=card_set)
    cards = FlashCard.objects.filter(card_set=card_set)
    if len(h) == 0:
        sum_cards = len(cards)
        for c in cards:
            if not c.front_first:
                sum_cards += 1
        h = SetHistory()
        h.card_set = card_set
        h.history = str(round(time.time())) + ":0" + (",0"*10) + "," + str(sum_cards)
    else:
        h = h[0]
    
    data = [0]*12
    for c in cards:
        if c.history == "":
            data[11] += 1
        else:
            idx = 5 - round(c.scoreFront() / 3)
            data[idx] += 1
        if not c.front_first:
            if c.history_back == "":
                data[11] += 1
            else:
                idx = 5 - round(c.scoreBack() / 3)
                data[idx] += 1
    new_entry = str(round(time.time())) + ":" + ",".join([str(d) for d in data])
    
    history = new_entry + ";" + h.history
    entries = history.split(";")
    if len(entries) == 12:
        timestamps = [int(entry.split(":")[0]) for entry in entries]
        time_diff = timestamps[-1] - timestamps[0]
        stepsize = time_diff / 10
        fitness = dict()
        for to_remove in range(1, 11):
            fitness[to_remove] = 0
            fitness[to_remove] += abs(timestamps[to_remove - 1] - timestamps[to_remove])
            fitness[to_remove] += abs(timestamps[to_remove + 1] - timestamps[to_remove])
        least_fit = min(fitness, key=fitness.get)
        entries.pop(least_fit)
        history = ";".join(entries)
        
    h.update(history=history)
        
def set_plot(request, set_id):
    if request.method == 'GET':
        
        card_set = CardSet.objects.get(pk=set_id)
        set_history = SetHistory.objects.filter(card_set=card_set)
        if len(set_history) == 0:
            make_snapshot(set_id)
            set_history = SetHistory.objects.filter(card_set=card_set)
        set_history = set_history[0]
        
        
        
        data = [[] for _ in range(12)]
        for x, entry in enumerate(set_history.history.split(";")[:-1]):
            ts, values = entry.split(':')
            for line_i, y in enumerate(reversed(values.split(','))):
                if y == '':
                    y = '0'
                data[line_i].append(int(y))
                
                
        for x in range(len(data[0])):
            csum = 0
            for line_i in reversed(range(len(data))):
                y = data[line_i][x]
                data[line_i][x] += csum
                csum += y
            for line_i in reversed(range(len(data))):
                data[line_i][x] /= csum
        
        
        
        
        colors = (
            "#cccccc",
            "#ff0000",
            "#ff3300",
            "#ff6600",
            "#ff9900",
            "#ffcc00",
            "#ffff00",
            "#b4e000",
            "#74c200",
            "#41a300",
            "#1b8500",
            "#006600"
        )
        
        
        fig = plt.figure()
        plt.title(card_set.name)
        
        for line_i, y in enumerate(data):
            print(y[::-1])
            x = range(len(y))[::-1]
            plt.fill_between(x, y, color=colors[line_i])
        
        canvas = FigureCanvas(fig)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        response = HttpResponse(buf.getvalue(), content_type='image/png')
        return response
        

def results(request, result):
    if request.method == 'GET':
        changed_sets = set()
        card_data_front, card_data_back, timestamp, marked_cards = result.split(";")
        if card_data_front != "":
            data = [pair.split(':') for pair in card_data_front.split(',')]
            for cardID, r in data:
                card = FlashCard.objects.get(pk=cardID)
                changed_sets.add(card.card_set.id)
                card.history = (r + card.history)[:16]
                card.last_trained_date = datetime.datetime.fromtimestamp(int(timestamp))
                if card.front_first:
                    card.last_trained_date_back = datetime.datetime.fromtimestamp(int(timestamp))
                card.save()
        if card_data_back != "":
            data = [pair.split(':') for pair in card_data_back.split(',')]
            for cardID, r in data:
                card = FlashCard.objects.get(pk=cardID)
                changed_sets.add(card.card_set.id)
                card.history_back = (r + card.history_back)[:16]
                card.last_trained_date = datetime.datetime.fromtimestamp(int(timestamp))
                card.last_trained_date_back = datetime.datetime.fromtimestamp(int(timestamp))
                card.save()
        if marked_cards != "":
            marked_ids = marked_cards.split(",")
            for cardID in marked_ids:
                card = FlashCard.objects.get(pk=cardID)
                card.marked = True
                card.save()
        
        for set_id in changed_sets:
            make_snapshot(set_id)
                
        return HttpResponse('Saved.')
        