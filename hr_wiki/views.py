from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'hr_wiki/home.html')
def home2(request):
    return render(request, 'hr_wiki/home2.html',{'name': 'home2'})