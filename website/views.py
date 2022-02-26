from django.shortcuts import render


def index(request):
    context = {
        'title_page': "Beranda"
    }
    return render(request, 'website/index.html', context)


def signin(request):
    context = {
        'title_page': "Masuk"
    }
    return render(request, 'website/signin.html', context)


def signup(request):
    context = {
        'title_page': "Daftar"
    }
    return render(request, 'website/signup.html', context)
