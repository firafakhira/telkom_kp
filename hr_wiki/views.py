from django.shortcuts import render
from .forms import LoginForm

# Create your views here.
def home(request):
    return render(request, 'hr_wiki/home.html')
    form = LoginForm()
    return render(request, 'hr_wiki/home.html', {'form': form})
  
def home2(request):
    return render(request, 'hr_wiki/home2.html',{'name': 'home2'})
  
def sear(request):
    return render(request, 'hr_wiki/search.html',{'name' :'search'})