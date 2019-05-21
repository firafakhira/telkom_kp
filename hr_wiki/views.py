from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'hr_wiki/home.html')
def sear(request):
    return render(request, 'hr_wiki/search.html',{'name' :'search'})