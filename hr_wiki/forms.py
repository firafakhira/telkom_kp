from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'placeholder': 'Password'
        }
    ))

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder': 'Type Here...',
            'class': 'inp_search'
        }
    ))

class LikeForm(forms.Form):
    like = forms.CharField(widget=forms.HiddenInput(
        attrs = {
            'value': '1'
        }
    ))

class DislikeForm(forms.Form):
    dislike = forms.CharField(widget=forms.HiddenInput(
        attrs = {
            'value': '1'
        }
    ))

class KomenForm(forms.Form):
    komen = forms.CharField(widget=forms.Textarea)
<<<<<<< HEAD
=======

class ShareForm(forms.Form):
    penerima = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder': 'NIK Penerima',
            'class': 'penerima'
        }
    ))

    at = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'at',
            'value': '@telkom.co.id',
            'readonly': ''
        }
    ))
>>>>>>> 66e60ec14cd5132505443047344905a0b08665db
