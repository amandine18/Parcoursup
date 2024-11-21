from django.db import models
from django.conf import settings

class Ecole(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nom

class Niveaux(models.Model):
    nom = models.CharField(max_length=10, unique=True)

    def __str__(self) :
        return self.nom

class Offres(models.Model):
    title = models.CharField(max_length=100)
    niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()

    def __str__(self) :
        return self.title + " - " + self.niveau.nom

class Postuler(models.Model):
    STATUT_CHOICES = [
        (0, 'En cours'),
        (1, 'Refusée'),
        (2, 'Acceptée'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True)
    lettre = models.TextField()
    offre = models.ForeignKey(Offres, on_delete=models.CASCADE)
    statut = models.IntegerField(choices=STATUT_CHOICES, default=0)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.offre.title}"