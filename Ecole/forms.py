from django import forms
from django.contrib.auth.models import User
from Parcoursup.models import *

class OffresForm(forms.ModelForm):
    class Meta:
        model = Offres
        fields = ['title', 'niveau', 'ecole', 'description']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    statut = forms.ChoiceField(choices=[('ecole', 'École')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'statut']