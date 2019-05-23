from django.shortcuts import render
from .forms import LoginForm, SearchForm
from django.core.paginator import Paginator
from .models import Konten

# Create your views here.
def home(request):
    form = LoginForm()
    return render(request, 'hr_wiki/home.html', {'form': form})
  
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

def content(request):
    return render(request, 'hr_wiki/content.html', {'name': 'content'})