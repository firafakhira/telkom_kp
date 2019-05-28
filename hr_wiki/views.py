from django.shortcuts import render, redirect
from .forms import LoginForm, SearchForm
from search.documents import KontenDocument
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from hr_wiki.models import Konten
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    form = LoginForm()
    return render(request, 'hr_wiki/home.html', {'form': form})
  
def home2(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            hasil = form.cleaned_data['search']
            link = f'http://localhost:8000/search/?q={hasil}'
            return redirect(link)
    else:
        form = SearchForm()
        return render(request, 'hr_wiki/home2.html', {'name': 'home2', 'form': form})
  
def sear(request):
    # konten_list = Konten.objects.all()
    # paginator = Paginator(konten_list, 5)
    # page = request.GET.get('page')
    # kontens = paginator.get_page(page)


    # form = SearchForm()
    # q = request.GET.get('q')
    # if q:
    #     konten = KontenDocument.search().query('match',judul=q)
    #     link = f'http://localhost:8000/search/?q=HRM'
    #     return redirect(link)
    # else:
    #     konten = ''
    # return render(request, 'hr_wiki/search.html', {'name': 'search', 'konten':konten, 'form':form})
    # else:
    #     form = SearchForm()
    #     return render(request, 'hr_wiki/search.html', {'name': 'search', 'konten':konten, 'form':form})
    if request.method == 'GET':
        q = request.GET.get('q')
        form = SearchForm()
        if q:
            konten = KontenDocument.search().query('match',judul=q)
        else:
            konten = ''
        link = 'http://localhost:8000/search/?q='+q
        #return redirect(link, {'name': 'search', 'konten':konten, 'form':form})
        return render(request, 'hr_wiki/search.html', {'name': 'search', 'konten':konten, 'form':form})
    elif request.method == 'POST':
        q = request.POST.get('q','')
        print(q)
        form = SearchForm()
        if q:
            konten = KontenDocument.search().query('match',judul=q)
        else:
            konten = ''
        link = 'http://localhost:8000/search/?q='+q
        return redirect(link, {'name': 'search', 'konten':konten, 'form':form})

def content(request):
    return render(request, 'hr_wiki/content.html', {'name': 'content'})