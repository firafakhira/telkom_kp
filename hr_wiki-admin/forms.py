from django import forms

class EditForm(forms.Form):
    isi = forms.CharField(widget=forms.Textarea(
        attrs = {
            'id': 'full-featured'
        }
    ))
    judul = forms.CharField(widget=forms.Textarea(
        attrs = {
            'id': 'basic-example'
        }
    ))