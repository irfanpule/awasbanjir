from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from perangkat.models import Perangkat


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


def about(request):
    context = {
        'title_page': "Tentang"
    }
    return render(request, 'website/about.html', context)

def get_point_devices(request):
    geojson = Perangkat.to_geojson(Perangkat.objects.all())
    return JsonResponse(geojson, status=200)
