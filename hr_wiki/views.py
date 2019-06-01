from django.shortcuts import render, redirect

#INI UNTUK IMPORT FORMS
from .forms import LoginForm, SearchForm, LikeForm, DislikeForm, KomenForm

#INI UNTUK PAGINATION BAGIAN SEARCH
from django.core.paginator import Paginator

#INI IMPORT MODEL
from .models import Incident, Log

#INI BUAT Q OBJECTS FILTER
from django.db.models import Q

#IMPORT DARI SEARCH UNTUK ELASTICSEARCH
from search.documents import IncidentDocument

#UNTUK STRIP
from django.utils.html import strip_tags

#UNTUK REGULAR EXPRESSION
import re

import math

import requests
import json

# Create your views here.
def landing(request):
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
                    return redirect('wiki-home')
                else:
                    # form = LoginForm()
                    # return render(request, 'hr_wiki/home.html', {'form': form})
                    return redirect('wiki-landing')
        else:
            form = LoginForm()
            return render(request, 'hr_wiki/landing.html', {'name': 'Landing','form': form})

    # INI BUAT LOAD API NYA DUDE
    # url = 'https://apifactory.telkom.co.id:8243/hcm/auth/v1/token?username=402256&password=Sflozi14'
    # r = requests.post(url)
    # status = [r.json]
  
def home(request):
    try:
        request.session['username']
    except KeyError:
        return redirect('wiki-landing')
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
            return render(request, 'hr_wiki/home.html', {'name': 'Home', 'form': form, 'username': request.session['username']})

  
def search(request, q):
    try:
        request.session['username']
    except KeyError:
        return redirect('wiki-landing')
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
            # konten = Konten.objects.filter(Q(judul__icontains=q) | Q(isi__icontains=q))
            konten_list = IncidentDocument.search().query("match_phrase_prefix", _all= q)
            # print(konten_list)
            konten = []
            for item in konten_list:
                konten.append(
                    {
                        'id': item.idincident,
                        'judul': item.kasus,
                        'highlight': strip_tags(item.solusi.replace("&nbsp;", ""))[:150]+'...',
                        'isi': strip_tags(item.solusi.replace("&nbsp;", ""))
                    }
                )
            paginator = Paginator(konten, 4)

            page = request.GET.get('page')
            kontens = paginator.get_page(page)
            return render(request, 'hr_wiki/search.html', {'name' :'Search', 'kontens': kontens, 'form': form, 'username': request.session['username']})

def content(request, content_id):
    try:
        request.session['username']
    except KeyError:
        return redirect('wiki-landing')
    except Exception:
        print('Error!')
    else:
        if request.method == 'POST':
                form = SearchForm(request.POST)
                like = LikeForm(request.POST)
                dislike = DislikeForm(request.POST)
                if form.is_valid():
                    q = form.cleaned_data['search']
                    red = f'http://localhost:8000/search/{q}'
                    return redirect(red)
                if like.is_valid():
                    l = like.cleaned_data['like']
                    likes = Incident.objects.get(idincident=content_id)
                    likes.like += int(l)
                    likes.save()
                    logs = Log(username=request.session['username'], like=True)
                    logs.incident_id = content_id
                    logs.save()

                    red = f'http://localhost:8000/content/{content_id}'
                    return redirect(red)
                if dislike.is_valid():
                    dl = dislike.cleaned_data['dislike']
                    dislikes = Incident.objects.get(idincident=content_id)
                    dislikes.dislike += int(dl)
                    dislikes.save()
                    logs = Log(username=request.session['username'], dislike=True)
                    logs.incident_id = content_id
                    logs.save()
                    
                    red = f'http://localhost:8000/content/{content_id}'
                    return redirect(red)
        else:
            content = Incident.objects.get(idincident=content_id)
            form = SearchForm()
            like = LikeForm()
            dislike = DislikeForm()
            komen = KomenForm()
            if (int(content.like) + int(content.dislike)) != 0:
                pLike = math.floor(int(content.like) / (int(content.like) + int(content.dislike)) * 5)
            else:
                pLike = 0
            stars = []
            for i in range(pLike):
                stars.append('<span class="fa fa-star checked"></span>')
            if pLike != 5:
                for i in range(5-pLike):
                    stars.append('<span class="fa fa-star"></span>')

            getLog = Log.objects.filter(Q(username=request.session['username']) & Q(incident_id=content_id) & Q(like=1) | Q(dislike=1))
            if len(getLog) != 0:
                disable = Log.objects.filter(Q(username=request.session['username']) & Q(incident_id=content_id)).first()
                return render(request, 'hr_wiki/content.html', {'name': 'Content', 'form': form, 'like': like, 'dislike': dislike, 'komen': komen, 'stars': stars, 'disable': disable, 'konten': content, 'username': request.session['username']})
            else:
                return render(request, 'hr_wiki/content.html', {'name': 'Content', 'form': form, 'like': like, 'dislike': dislike, 'komen': komen, 'stars': stars, 'konten': content, 'username': request.session['username']})
                
            
