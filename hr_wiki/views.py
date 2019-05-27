from django.shortcuts import render

#INI UNTUK IMPORT FORMS
from .forms import LoginForm, SearchForm

#INI UNTUK PAGINATION BAGIAN SEARCH
from django.core.paginator import Paginator

#INI IMPORT MODEL
from .models import Konten

import requests
import json

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            url = f'https://apifactory.telkom.co.id:8243/hcm/auth/v1/token?username={username}&password={password}'
            response = requests.post(url)
            data = response.json()
            if data['status'] == 'success':
                form = SearchForm()
                return render(request, 'hr_wiki/home2.html', {'name': 'home2', 'form': form})
            else:
                form = LoginForm()
                return render(request, 'hr_wiki/home.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'hr_wiki/home.html', {'form': form})

    # INI BUAT LOAD API NYA DUDE
    # url = 'https://apifactory.telkom.co.id:8243/hcm/auth/v1/token?username=402256&password=Sflozi14'
    # r = requests.post(url)
    # status = [r.json]
  
def home2(request):
    form = SearchForm()
    return render(request, 'hr_wiki/home2.html', {'name': 'home2', 'form': form})
  
def sear(request):
    form = SearchForm()

    konten_list = Konten.objects.all()
    paginator = Paginator(konten_list, 5)

    page = request.GET.get('page')
    kontens = paginator.get_page(page)
    return render(request, 'hr_wiki/search.html', {'name' :'search', 'kontens': kontens, 'form': form})

def content(request, content_id):
    content = Konten.objects.get(id=content_id)
    form = SearchForm()
    judul = content.judul
    isi = content.isi.split('\n')
    return render(request, 'hr_wiki/content.html', {'name': 'content', 'form': form, 'judul': judul, 'isi': isi})