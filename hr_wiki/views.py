from django.shortcuts import render, redirect

#INI UNTUK IMPORT FORMS
from .forms import LoginForm, SearchForm

#INI UNTUK PAGINATION BAGIAN SEARCH
from django.core.paginator import Paginator

#INI IMPORT MODEL
from .models import Konten

#INI BUAT Q OBJECTS FILTER
from django.db.models import Q

#IMPORT DARI SEARCH
from search.documents import KontenDocument

#UNTUK STRIP
from django.utils.html import strip_tags

#UNTUK SPLIT
import re

import requests
import json

# Create your views here.
def home(request):
    if 'action' in request.GET:
        if request.GET.get('action') == 'logout':
            request.session.flush()
            return redirect('wiki-home')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                url = f'https://apifactory.telkom.co.id:8243/hcm/auth/v1/token?username={username}&password={password}'
                response = requests.post(url)
                data = response.json()
                if data['status'] == 'success':
                    # form = SearchForm()
                    request.session['username'] = username
                    request.session['token'] = data['data']['jwt']['token']
                    request.session.set_expiry(data['data']['jwt']['expires'])
                    # return render(request, 'hr_wiki/home2.html', {'name': 'home2', 'form': form, 'username': request.session['username']})
                    return redirect('wiki-home2')
                else:
                    # form = LoginForm()
                    # return render(request, 'hr_wiki/home.html', {'form': form})
                    return redirect('wiki-home')
        else:
            form = LoginForm()
            return render(request, 'hr_wiki/home.html', {'form': form})

    # INI BUAT LOAD API NYA DUDE
    # url = 'https://apifactory.telkom.co.id:8243/hcm/auth/v1/token?username=402256&password=Sflozi14'
    # r = requests.post(url)
    # status = [r.json]
  
def home2(request):
    try:
        request.session['username']
    except KeyError:
        return redirect('wiki-home')
    except Exception:
        print('Error!')
    else:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                q = form.cleaned_data['search']
                red = f'http://localhost:8000/search/{q}'
                return redirect(red)
        else:
            form = SearchForm()
            return render(request, 'hr_wiki/home2.html', {'name': 'home2', 'form': form, 'username': request.session['username']})

  
def sear(request, q):
    try:
        request.session['username']
    except KeyError:
        return redirect('wiki-home')
    except Exception:
        print('Error!')
    else:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                q = form.cleaned_data['search']
                red = f'http://localhost:8000/search/{q}'
                return redirect(red)
        else:
            form = SearchForm()
            konten = Konten.objects.filter(Q(judul__icontains=q) | Q(isi__icontains=q))
            konten_list = KontenDocument.search().query("match", judul= q)
            # print(konten_list)
            konten = []
            for item in konten_list:
                konten.append(
                    {
                        'id': item.id,
                        'judul': item.judul,
                        'highlight': strip_tags(item.isi)[:150]+'...',
                        'isi': strip_tags(item.isi)
                    }
                )
            paginator = Paginator(konten, 4)

            page = request.GET.get('page')
            kontens = paginator.get_page(page)
            return render(request, 'hr_wiki/search.html', {'name' :'search', 'kontens': kontens, 'form': form, 'username': request.session['username']})

def content(request, content_id):
    content = Konten.objects.get(id=content_id)
    form = SearchForm()
    judul = content.judul
    isi = content.isi.split('\n')
    print(isi[0][:150]+'...')
    # for i in range(len(isi)):
    #     isi[i] = strip_tags(isi[i]) + '\n'
    return render(request, 'hr_wiki/content.html', {'name': 'content', 'form': form, 'judul': judul, 'isi': isi, 'username': request.session['username']})