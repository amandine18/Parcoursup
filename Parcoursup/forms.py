from django import forms
from Parcoursup.models import Postuler
from django.contrib.auth.models import User
from .models import *

class OffreForm(forms.ModelForm):
    class Meta:
        model = Postuler
        fields = ['nom', 'prenom','lettre']

class OffresForm(forms.ModelForm):
    class Meta:
        model = Offres
        fields = ['title', 'niveau', 'ecole', 'description']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    statut = forms.ChoiceField(choices=[('etudiant', 'Étudiant')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'statut']