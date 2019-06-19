from django.shortcuts import render, redirect

#INI UNTUK IMPORT FORMS
from .forms import LoginForm, SearchForm, LikeForm, DislikeForm, KomenForm, ShareForm

#INI UNTUK PAGINATION BAGIAN SEARCH
from django.core.paginator import Paginator

#INI UNTUK FLASH MESSAGE
from django.contrib import messages

#INI IMPORT MODEL
from .models import Incident, Komentar

#INI BUAT Q OBJECTS FILTER
from django.db.models import Q

#IMPORT DARI SEARCH UNTUK ELASTICSEARCH
from search.documents import IncidentDocument

#UNTUK STRIP
from django.utils.html import strip_tags

#UNTUK REGULAR EXPRESSION
import re

#UNTUK SHARE LINK VIA EMAIL
from django.core.mail import send_mail
from django.conf import settings

from hc_wiki.services import update_log_incident, find_log, count_stars, get_highlight, get_expired

import requests
import json

from elasticsearch import Elasticsearch

# Create your views here.
def landing(request):
    try:
        request.session['username']
    except KeyError:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                url = f'https://apifactory.telkom.co.id:8243/hcm/auth/v1/token?username={username}&password={password}'
                response = requests.post(url)
                data = response.json()
                if data['status'] == 'success':
                    request.session['username'] = username
                    request.session['password'] = password
                    request.session['token'] = data['data']['jwt']['token']
                    request.session.set_expiry(get_expired(data['data']['jwt']['expires']))
                    messages.success(request, 'You are Logged In!')

                    headers = {}
                    headers['x-authorization'] = f"Bearer {request.session['token']}"

                    url = f"https://apifactory.telkom.co.id:8243/hcm/employee/v1/getEmployee/v1/1/{request.session['username']}"

                    response = requests.get(url, headers=headers)

                    print(response.text)

                    return redirect('wiki-home')
                else:
                    messages.error(request, 'Incorrect Username or Password!')
                    return redirect('wiki-landing')
        else:
            form = LoginForm()
            return render(request, 'hc_wiki/landing.html', {'name': 'Landing','form': form})
    except Exception:
        print('Error!')
    else:
        if 'action' in request.GET:
            if request.GET.get('action') == 'logout':
                request.session.flush()
                messages.success(request, 'You are Logged Out!')
                return redirect('wiki-home')
        else:
            return redirect('wiki-home')
  
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
            return render(
                            request, 
                            'hc_wiki/home.html', 
                            {
                                'name': 'Home', 
                                'form': form, 
                                'username': request.session['username']
                            }
            )

  
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
            db = Incident.objects.all()

            konten_list = Elasticsearch('10.60.185.217:9200').search(index="incident", body={
                'query': {
                    'multi_match': {
                        'query': q,
                        'fields' : ['kasus', 'solusi', 'applikasi',],
                        'type': 'phrase_prefix',
                    }
                },
                'from': 0 , 'size': len(db),
                'sort': [{'hits': {'order': 'desc'}}]
            })
            konten = []
            for item in konten_list['hits']['hits']:
                konten.append(
                    {
                        'id': item['_source']['idincident'],
                        'judul': item['_source']['kasus'].replace("&nbsp;", ""),
                        'hilite': get_highlight(item['_source']['kasus'].replace("&nbsp;", ""), 3),
                        'highlight': get_highlight(item['_source']['solusi'].replace("&nbsp;", "")),
                        'isi': item['_source']['solusi'].replace("&nbsp;", ""),
                        'views': item['_source']['hits'],
                    }
                )

            # konten = sorted(konten, key=lambda x: x['views'], reverse=True)
            
            paginator = Paginator(konten, 4)
            print(paginator)

            page = request.GET.get('page')
            kontens = paginator.get_page(page)
            return render(
                            request, 
                            'hc_wiki/search.html', 
                            {
                                'name' :'Search', 
                                'kontens': kontens, 
                                'form': form, 
                                'username': request.session['username']
                            }
            )

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
                komen = KomenForm(request.POST)

                if form.is_valid():
                    q = form.cleaned_data['search']
                    red = f'http://localhost:8000/search/{q}'
                    return redirect(red)
                if like.is_valid():
                    likes = Incident.objects.get(idincident=content_id)
                    update_log_incident('like', likes, request.session['username'], content_id)

                    red = f'http://localhost:8000/content/{content_id}'
                    return redirect(red)
                if dislike.is_valid():
                    dislikes = Incident.objects.get(idincident=content_id)
                    update_log_incident('dislike', dislikes, request.session['username'], content_id)
                    
                    red = f'http://localhost:8000/content/{content_id}'
                    return redirect(red)
                if komen.is_valid():
                    isiKomen = komen.cleaned_data['komen']

                    saveKomen = Komentar(nik=request.session['username'], isi_komentar=isiKomen)
                    saveKomen.incident_id = content_id
                    saveKomen.save()

                    messages.success(request, "Thanks for your comment!")

                    red = f'http://localhost:8000/content/{content_id}'
                    return redirect(red)
        else:
            content = Incident.objects.get(idincident=content_id)
            form = SearchForm()
            like = LikeForm()
            dislike = DislikeForm()
            komen = KomenForm()
            share = ShareForm()
            
            #INI UNTUK ARTIKEL TERKAIT
            artikel_terkait = Incident.objects.filter(applikasi=content.applikasi)[:5]
            for i in range(len(artikel_terkait)):
                artikel_terkait[i].hilite = get_highlight(artikel_terkait[i].kasus, 3)

            #INI UNTUK GET KOMENTAR
            comment = Komentar.objects.filter(incident_id=content_id)

            #INI UNTUK DIBAWA KE URL SHARE BIAR BISA BALIK KE SINI
            request.session['content_id'] = content_id

            stars = count_stars(content)

            update_log_incident('hits', content, request.session['username'], content_id)

            findLog = find_log(request.session['username'], content_id)

            likeDisIsThere = findLog.filter(Q(like = True) | Q(dislike = True))
            if len(likeDisIsThere) != 0:
                disable = findLog.first()

                return render(
                                request, 
                                'hc_wiki/content.html', 
                                {
                                    'name': 'Content', 
                                    'form': form, 
                                    'like': like, 
                                    'dislike': dislike, 
                                    'komen': komen, 
                                    'share': share, 
                                    'stars': stars, 
                                    'disable': disable, 
                                    'konten': content,
                                    'artikels': artikel_terkait,
                                    'comment' : comment,
                                    'username': request.session['username']
                                }
                )
            else:
                return render(
                                request, 
                                'hc_wiki/content.html', 
                                {
                                    'name': 'Content',
                                    'form': form,
                                    'like': like,
                                    'dislike': dislike,
                                    'komen': komen,
                                    'share': share,
                                    'stars': stars,
                                    'konten': content,
                                    'artikels': artikel_terkait,
                                    'comment' : comment,
                                    'username': request.session['username']
                                }
                )

def share_link(request):
    if 'url' in request.GET:
        if request.GET.get('url'):
            if request.method == 'POST':
                share = ShareForm(request.POST)
                if share.is_valid():
                    nik = share.cleaned_data['penerima']
                    at = share.cleaned_data['at']
                    subjekEmail = "HC-Wiki Share Link"
                    isiEmail = f'Check this link: http://localhost:8000{request.GET.get("url")}'
                    pengirim = f'{request.session["username"]}@telkom.co.id'
                    penerima = f'{nik}{at}'

                    settings.EMAIL_HOST_USER = pengirim
                    settings.EMAIL_HOST_PASSWORD = request.session['password']

                    send_mail(subjekEmail,isiEmail,pengirim,[penerima],fail_silently=False,)

                    messages.success(request, f'This link was successfully shared to {penerima}')
                    
                    red = f'http://localhost:8000/content/{request.session["content_id"]}'
                    return redirect(red)