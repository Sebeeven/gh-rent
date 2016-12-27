from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=1)
    password = forms.CharField(min_length=1)

class CreateForm(forms.Form):
    username = forms.CharField(min_length=1)
    password = forms.CharField(min_length=1)
    email = forms.EmailField(min_length=1)
    vocation = forms.CharField()

class ModifyForm(forms.Form):
    username = forms.CharField(min_length=1)
    password = forms.CharField(min_length=1)
