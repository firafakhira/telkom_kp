from django.shortcuts import render, redirect
from hr_wiki.models import Incident
from hr_wiki.services import get_highlight
import re
from .forms import EditForm

#INI UNTUK FLASH MESSAGE
from django.contrib import messages

# Create your views here.
def login(request):

    return render(request, 'hr_wiki-admin/login.html', {'name': 'login',})

def home(request):
    Data = Incident.objects.all()

    konten = []
    base_patterns = {
        '&[rl]dquo;': '',
        '&[rl]squo;': '',
        '&nbsp;': ''
    }

    for i in range(len(Data)):
        for pattern, repl in base_patterns.items():
                Data[i].solusi = re.sub(pattern, repl, Data[i].solusi)
        Data[i].highlight = get_highlight(Data[i].solusi)

    return render(request, 'hr_wiki-admin/home.html', {'name': 'home','data':Data})

def editKonten(request, content_id):
    if request.method == 'POST':
        areaForm = EditForm(request.POST)
        if areaForm.is_valid():
            judul = areaForm.cleaned_data['judul']
            isi = areaForm.cleaned_data['isi']

            content = Incident.objects.get(idincident=content_id)
            content.kasus = judul
            content.solusi = isi
            content.save()
            
            messages.success(request, f'ID {content_id} was succesfully updated!')

            red = f'http://localhost:8000/admin/edit/{content_id}'
            return redirect(red)
    else:
        content = Incident.objects.get(idincident=content_id)
        areaForm = EditForm(initial={'isi': content.solusi, 'judul': content.kasus})
        return render(request, 'hr_wiki-admin/edit.html', {'name': 'edit','content':content, 'form': areaForm})