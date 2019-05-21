from django.shortcuts import render
from .forms import LoginForm

# Create your views here.
def home(request):
    form = LoginForm()
    return render(request, 'hr_wiki/home.html', {'form': form})