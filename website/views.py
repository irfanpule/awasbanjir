from django.shortcuts import render
from django.conf import settings


def index(request):
    context = {
        'title_page': "Beranda",
        'mapbox_key': settings.MAPBOX_KEY
    }
    return render(request, 'website/index.html', context)


def signup(request):
    context = {
        'title_page': "Daftar"
    }
    return render(request, 'website/signup.html', context)
