from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from Parcoursup.forms import OffreForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Parcoursup.models import Offres, Postuler
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('index')

def offre_list(request):
    offres = Offres.objects.all()
    return render(request, 'parcoursup/indexetud.html', {'offres':offres})

def home(request):
    return render(request, 'parcoursupecole/home.html')

def profiletud(request):
    candidatures = Postuler.objects.filter(user=request.user)  # Récupère toutes les candidatures de l'utilisateur
    total_candidatures = len(candidatures)
    return render(request, 'parcoursup/profiletud.html', {
        'candidatures': candidatures,
        'total_candidatures': total_candidatures
    })

def candidater(request, pk):
    offre = get_object_or_404(Offres, pk=pk)
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            candidature = form.save(commit=False)  # On ne sauve pas encore dans la DB
            candidature.offre = offre  # Lier la candidature à l'offre
            candidature.email = request.user.email
            candidature.user = request.user
            candidature.save()
            messages.success(request, "Votre candidature a été soumise avec succès.")
            return redirect('index')
    else:
        form = OffreForm()
    return render(request, 'Parcoursup/create_candidate.html', {'form': form, 'offre': offre})


def mes_candidatures(request):
    if request.user.is_authenticated:
        candidatures = Postuler.objects.filter(user=request.user)  # Récupère toutes les candidatures de l'utilisateur
        return render(request, 'parcoursup/candidatures.html', {'candidatures': candidatures})
    else:
        messages.error(request, "Vous devez être connecté pour voir vos candidatures.")
        return redirect('loginetud')
    
    
def update_candidature(request, pk):
    candidate = get_object_or_404(Postuler, pk=pk)
    if request.method == 'POST':
        form = OffreForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('candidatures')
    else:
        form = OffreForm(instance=candidate)
    return render(request, 'parcoursup/update_candidate.html', {'form': form, 'candidate': candidate})


def delete_candidature(request, pk):
    candidate = get_object_or_404(Postuler, pk=pk)
    if request.method == 'POST':
        candidate.delete()
        return redirect('candidatures')
    return render(request, 'parcoursup/delete_candidate.html', {'candidate': candidate})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Identifiants invalides.")
        else:
            messages.error(request, "Formulaire invalide.")
    else:
        form = AuthenticationForm() 
    return render(request, 'parcoursup/loginetud.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Inscription réussie, vous pouvez maintenant vous connecter.")
            return redirect('loginetud')  # Redirigez vers la page de connexion
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = UserRegistrationForm()
    return render(request, 'parcoursup/registeretud.html', {'form': form})
