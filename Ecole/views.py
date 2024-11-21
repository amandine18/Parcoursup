from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Parcoursup.models import *
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect

class CustomLogoutView1(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')

def offre_list(request):
    offres = Offres.objects.all()
    return render(request, 'ecole/home.html', {'offres':offres})

def index_etud(request):
    return render(request, 'parcoursup/indexetud.html')

# def profil(request):
#     candidatures = Postuler.objects.filter(ecole=request.user)  # Récupère toutes les candidatures de l'utilisateur
#     total_candidatures = len(candidatures)
#     return render(request, 'parcoursupecole/profilecole.html', {
#         'candidatures': candidatures,
#         'total_candidatures': total_candidatures
#     })

def profilecole(request):
    # Récupère l'école spécifique
    ecole = get_object_or_404(Ecole, nom=request.user.username)
    
    # Récupère toutes les offres de l'école
    offres_de_l_ecole = Offres.objects.filter(ecole=ecole)
    
    # Compte le nombre de candidatures pour les offres de cette école
    total_candidate = Postuler.objects.filter(offre__in=offres_de_l_ecole).count()
    candidates = Postuler.objects.filter(offre__in=offres_de_l_ecole)
    
    return render(request, 'ecole/profilecole.html', {
        'ecole': ecole,
        'total_candidate': total_candidate,
        'candidates': candidates
    })

@csrf_protect
def update_statut(request, candidate_id):
    candidate = get_object_or_404(Postuler, id=candidate_id)

    # Vérifie que la requête est bien un POST
    if request.method == "POST":
        # Récupère le nouveau statut depuis le formulaire
        new_statut = request.POST.get("statut")
        if new_statut is not None:
            candidate.statut = new_statut
            candidate.save()
    
    # Redirige vers la page de profil après la mise à jour
    return redirect('profilecole')

def create_offre(request):
    if request.method == 'POST':
        form = OffresForm(request.POST)
        if form.is_valid():
            create = form.save(commit=False)  # On ne sauve pas encore dans la DB
            create.user = request.user
            ecole_instance = get_object_or_404(Ecole, nom=request.user.username)
            create.ecole = ecole_instance
            form.save()
            messages.success(request, "Votre offre a été crée avec succès.")
            return redirect('home')
    else:
        form = OffresForm()
    return render(request, 'ecole/create_offre.html', {'form': form})

def mes_offres(request):
    if request.user.is_authenticated:
        try:
            ecole = Ecole.objects.get(nom=request.user.username)
            # Filtrer les offres associées à cette école
            offres = Offres.objects.filter(ecole=ecole)
            return render(request, 'ecole/offres.html', {'offres': offres})
        except Ecole.DoesNotExist:
            messages.error(request, "Aucune école associée à votre compte.")
            return redirect('home')
    else:
        messages.error(request, "Vous devez être connecté pour voir vos offres.")
        return redirect('loginecole')
    
def update_offre(request, pk):
    offre = get_object_or_404(Offres, pk=pk)
    if request.method == 'POST':
        form = OffresForm(request.POST, instance=offre)
        if form.is_valid():
            create = form.save(commit=False)  # On ne sauve pas encore dans la DB
            create.user = request.user
            ecole_instance = get_object_or_404(Ecole, nom=request.user.username)
            create.ecole = ecole_instance
            form.save()
            return redirect('offres')
    else:
        form = OffresForm(instance=offre)
    return render(request, 'ecole/update_offre.html', {'form': form, 'offre': offre})

def delete_offre(request, pk):
    offre = get_object_or_404(Offres, pk=pk)
    if request.method == 'POST':
        offre.delete()
        return redirect('offres')
    return render(request, 'ecole/delete_offre.html', {'offre': offre})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Identifiants invalides.")
        else:
            messages.error(request, "Formulaire invalide.")
    else:
        form = AuthenticationForm() 
    return render(request, 'ecole/loginecole.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            ecole = Ecole.objects.create(
                nom=user.username  # Associer le nom de l'école avec le username de l'utilisateur
            )
            ecole.save()

            messages.success(request, "Inscription réussie, vous pouvez maintenant vous connecter.")
            return redirect('loginecole')  # Redirigez vers la page de connexion
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = UserRegistrationForm()
    return render(request, 'ecole/registerecole.html', {'form': form})