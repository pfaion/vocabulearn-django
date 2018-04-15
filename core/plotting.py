from django.http import HttpResponse, JsonResponse
from .models import FlashCard, CardSet, Folder, SetHistory
import pickle 
import datetime
import time
import io

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd

from . import API

def get_set_plot_data(card_set):
    set_history = SetHistory.objects.filter(card_set=card_set)
    if len(set_history) == 0:
        API.make_snapshot(card_set.id)
        set_history = SetHistory.objects.filter(card_set=card_set)
    set_history = set_history[0]
    
    data = pd.DataFrame()
    for x, entry in enumerate(set_history.history.split(";")[:-1]):
        ts, values = entry.split(':')
        for line_i, y in enumerate(reversed(values.split(','))):
            if y == '':
                y = '0'
            data.loc[ts, line_i] = int(y)
            
    data.index = pd.DatetimeIndex(data.index.astype(float) * 1e9)
    data = data.sort_index()
    return data

def make_plot_reponse(data):
    data = data.iloc[:, ::-1].cumsum(axis=1).iloc[:, ::-1]
    data = data.div(data.iloc[:,0], axis=0)

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
    
    for line_i, column in enumerate(data.columns):
        y = data[column]
        x = range(len(y))
        plt.fill_between(x, y, color=colors[line_i])
    
    plt.xlim(0, len(data[0]) - 1)
    plt.ylim(0, 1)
    plt.axis('off')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    
    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches = 0)
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

def multi_set_plot(sets):
    all_sets_data = []
    for card_set in sets:
        set_data = get_set_plot_data(card_set)
        all_sets_data.append(set_data)
        
    new_index = all_sets_data[0].index
    for data in all_sets_data[1:]:
        new_index = new_index.union(data.index)
        
    for i, data in enumerate(all_sets_data):
        all_sets_data[i] = data.reindex(new_index).fillna(method='ffill').fillna(0.0)
        
    data = all_sets_data[0]
    for d in all_sets_data[1:]:
        data += d

    return make_plot_reponse(data)
    
def all_plot(request):
    if request.method == 'GET':
        
        sets = CardSet.objects.all()
        
        return multi_set_plot(sets)
        

def folder_plot(request, folder_id):
    if request.method == 'GET':
        
        folder = Folder.objects.get(pk=folder_id)
        sets = CardSet.objects.filter(folder=folder)
        
        return multi_set_plot(sets)
    
        
def set_plot(request, set_id):
    if request.method == 'GET':
        
        card_set = CardSet.objects.get(pk=set_id)
        data = get_set_plot_data(card_set)
        
        return make_plot_reponse(data)