from django import forms


class customer(forms.Form):
    name=forms.CharField(label='Name',max_length=100)
    email=forms.EmailField(label='Email')
    password=forms.CharField(label='password')