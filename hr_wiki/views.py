from django.shortcuts import render
<<<<<<< HEAD

# Create your views here.
def home(request):
    return render(request, 'hr_wiki/home.html')
=======
from .forms import LoginForm, SearchForm

# Create your views here.
def home(request):
    form = LoginForm()
    return render(request, 'hr_wiki/home.html', {'form': form})
  
def home2(request):
    form = SearchForm()
    return render(request, 'hr_wiki/home2.html',{'name': 'home2', 'form': form})
  
>>>>>>> 0b8a0203fee861eb23577fa5851df7e1b4f179fa
def sear(request):
    return render(request, 'hr_wiki/search.html',{'name' :'search'})