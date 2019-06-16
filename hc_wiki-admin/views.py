from django.shortcuts import render, redirect
from hc_wiki.models import Incident
from hc_wiki.services import get_highlight
import re
from .forms import IncidentForm

#INI UNTUK FLASH MESSAGE
from django.contrib import messages

# Create your views here.
def login(request):

    return render(request, 'hc_wiki-admin/login.html', {'name': 'login',})

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

    return render(request, 'hc_wiki-admin/home.html', {'name': 'home','data':Data})

def editKonten(request, content_id):
    if request.method == 'POST':
        areaForm = IncidentForm(request.POST)
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
        areaForm = IncidentForm(initial={'isi': content.solusi, 'judul': content.kasus})
        return render(request, 'hc_wiki-admin/edit.html', {'name': 'edit','content':content, 'form': areaForm})

# def addKonten(request):
#     if request.method == 'POST':
#         areaForm = IncidentForm(request.POST)
#         if areaForm.is_valid():
#             judul = areaForm.cleaned_data['judul']
#             isi = areaForm.cleaned_data['isi']

#             content = Incident(kasus=judul, solusi=isi)
#             content.save()
            
#             messages.success(request, f'Content was succesfully created!')

#             red = f'http://localhost:8000/admin/add/'
#             return redirect('admin-home')
#     else:
#         areaForm = IncidentForm()
#         return render(request, 'hc_wiki-admin/add.html', {'name': 'add', 'form': areaForm})

# def deleteKonten(request, content_id):
#     delete = Incident.objects.get(idincident=content_id)
#     delete.delete()

#     messages.success(request, f'Content was succesfully deleted!')

#     return redirect('admin-home')