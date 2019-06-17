from django.shortcuts import render, redirect

#IMPORT DATABASE DARI APP HC_WIKI
from hc_wiki.models import Incident

#IMPORT SERVICES DARI APP HC_WIKI
from hc_wiki.services import get_highlight

#REGULAR EXPRESSION
import re

#IMPORT FORM
from .forms import IncidentForm
from hc_wiki.forms import LoginForm

#INI UNTUK FLASH MESSAGE
from django.contrib import messages

#IMPORT WAKTU
from datetime import datetime

# Create your views here.
def login(request):
    try:
        request.session['admin']
    except KeyError:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                if username == 'admin' and password == 'admin':
                    request.session['admin'] = username
                    request.session.set_expiry(3600)

                    messages.success(request, 'You are Logged In!')

                    return redirect('admin-home')
                else:
                    return redirect('admin-login')
        else:
            form = LoginForm()

            return render(request, 'hc_wiki-admin/login.html', {'name': 'login', 'form': form})
    except Exception as e:
        print(e)
    else:
        if 'action' in request.GET:
            if request.GET.get('action') == 'logout':
                request.session.flush()
                messages.success(request, 'You are Logged Out!')
                return redirect('admin-login')

    


def home(request):
    try:
        request.session['admin']
    except KeyError:
        return redirect('admin-login')
    except Exception as e:
        print(e)
    else:
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

        return render(request, 'hc_wiki-admin/home.html', {'name': 'home', 'data':Data, 'admin': request.session['admin']})

def editKonten(request, content_id):
    try:
        request.session['admin']
    except KeyError:
        return redirect('admin-login')
    except Exception as e:
        print(e)
    else:
        if request.method == 'POST':
            areaForm = IncidentForm(request.POST)
            if areaForm.is_valid():
                judul = areaForm.cleaned_data['judul']
                isi = areaForm.cleaned_data['isi']
                tema = areaForm.cleaned_data['tema']

                content = Incident.objects.get(idincident=content_id)
                content.kasus = judul
                content.solusi = isi
                content.applikasi = tema
                content.lastupdate = datetime.now()
                content.save()
                
                messages.success(request, f'ID {content_id} was succesfully updated!')

                return redirect('admin-home')
        else:
            content = Incident.objects.get(idincident=content_id)
            areaForm = IncidentForm(initial={'isi': content.solusi, 'judul': content.kasus, 'tema': content.applikasi})
            return render(request, 'hc_wiki-admin/add_edit.html', {'name': 'Edit Konten','content':content, 'form': areaForm, 'admin': request.session['admin']})

def addKonten(request):
    try:
        request.session['admin']
    except KeyError:
        return redirect('admin-login')
    except Exception as e:
        print(e)
    else:
        if request.method == 'POST':
            areaForm = IncidentForm(request.POST)
            if areaForm.is_valid():
                judul = areaForm.cleaned_data['judul']
                isi = areaForm.cleaned_data['isi']
                tema = areaForm.cleaned_data['tema']

                content = Incident(kasus=judul, solusi=isi, applikasi=tema, createdby=request.session['admin'])
                content.save()
                
                messages.success(request, f'Content was succesfully created!')

                return redirect('admin-home')
        else:
            areaForm = IncidentForm()
            return render(request, 'hc_wiki-admin/add_edit.html', {'name': 'Create Konten', 'form': areaForm, 'admin': request.session['admin']})

def deleteKonten(request, content_id):
    try:
        request.session['admin']
    except KeyError:
        return redirect('admin-login')
    except Exception as e:
        print(e)
    else:
        delete = Incident.objects.get(idincident=content_id)
        delete.delete()

        messages.success(request, f'Content was succesfully deleted!')

        return redirect('admin-home')