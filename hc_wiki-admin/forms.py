from django import forms

class IncidentForm(forms.Form):
    isi = forms.CharField(widget=forms.Textarea(
        attrs = {
            'id': 'full-featured'
        }
    ),required=False)
    judul = forms.CharField(widget=forms.Textarea(
        attrs = {
            'id': 'basic-example'
        }
    ),required=False)