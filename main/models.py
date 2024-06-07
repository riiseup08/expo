# main/models.py

from django.db import models
from django.contrib.auth.models import User

class Voyageur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    date_depart = models.DateField()
    date_arrivee = models.DateField()
    poids_disponible = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Colis(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    poids = models.PositiveIntegerField()
    dimensions = models.CharField(max_length=100)

    def __str__(self):
        return f"Colis de {self.client.user.username}"

class Commande(models.Model):
    voyageur = models.ForeignKey(Voyageur, on_delete=models.CASCADE)
    colis = models.ForeignKey(Colis, on_delete=models.CASCADE)
    date_ramassage = models.DateField()
    date_livraison = models.DateField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Commande pour {self.colis.client.user.username}"

