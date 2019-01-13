from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from .models import FlashCard, CardSet, Folder, SetHistory
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import datetime
import time
import io
import jwt
from pprint import pprint


def token_authentication(func):
    def wrapper(request, *args):
        key = 'HTTP_CUSTOM_TOKEN'
        if key not in request.META:
            return JsonResponse({'Error': 'No authentication token present!'}, status='400')
        token = request.META[key]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        username = payload['username']
        password = payload['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'Error': 'Username and/or password were incorrect!'}, status='400')
        return func(request, *args)
    return csrf_exempt(wrapper)


@token_authentication
def debug(request):
    if request.method == 'POST':
        return JsonResponse({'Result': 'Success!'})


