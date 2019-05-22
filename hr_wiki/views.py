from django.shortcuts import render
from .forms import LoginForm, SearchForm

# Create your views here.
def home(request):
    form = LoginForm()
    return render(request, 'hr_wiki/home.html', {'form': form})
  
def home2(request):
    form = SearchForm()
    return render(request, 'hr_wiki/home2.html', {'name': 'home2', 'form': form})
  
def sear(request):
    return render(request, 'hr_wiki/search.html', {'name' :'search'})

def content(request):
    return render(request, 'hr_wiki/content.html', {'name': 'content'})