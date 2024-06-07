# Create your views here.
# main/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Voyageur, Client, Colis, Commande
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def accueil(request):
    return render(request, 'main/accueil.html')

def calculer_prix(poids):
    # Fonction pour calculer le prix en fonction du poids
    return poids * 2  # Exemple simplifié

def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        client = Client.objects.create(user=user)
        return redirect('login')
    return render(request, 'main/inscription.html')

def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('rechercher_commandes')
    return render(request, 'main/connexion.html')

@login_required
def rechercher_commandes(request):
    if request.method == 'POST':
        ville_depart = request.POST.get('ville_depart')
        ville_arrivee = request.POST.get('ville_arrivee')
        date_depart = request.POST.get('date_depart')
        date_arrivee = request.POST.get('date_arrivee')
        poids = request.POST.get('poids')
        voyageurs = Voyageur.objects.filter(
            ville_depart=ville_depart,
            ville_arrivee=ville_arrivee,
            date_depart=date_depart,
            date_arrivee=date_arrivee,
            poids_disponible__gte=poids
        )
        return render(request, 'main/rechercher_commandes.html', {'voyageurs': voyageurs})
    return render(request, 'main/rechercher_commandes.html')

@login_required
def creer_commande(request, voyageur_id):
    voyageur = get_object_or_404(Voyageur, id=voyageur_id)
    if request.method == 'POST':
        poids = request.POST.get('poids')
        dimensions = request.POST.get('dimensions')
        colis = Colis.objects.create(
            client=request.user.client,
            poids=poids,
            dimensions=dimensions
        )
        commande = Commande.objects.create(
            voyageur=voyageur,
            colis=colis,
            date_ramassage=voyageur.date_depart,
            date_livraison=voyageur.date_arrivee,
            prix=calculer_prix(int(poids))
        )
        return redirect('commande_details', commande.id)
    return render(request, 'main/creer_commande.html', {'voyageur': voyageur})

@login_required
def commande_details(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'main/commande_details.html', {'commande': commande})

@login_required
def mes_commandes(request):
    voyageur = Voyageur.objects.filter(user=request.user).first()
    client = Client.objects.filter(user=request.user).first()
    commandes_voyageur = Commande.objects.filter(voyageur=voyageur)
    commandes_client = Commande.objects.filter(colis__client=client)
    return render(request, 'main/mes_commandes.html', {
        'commandes_voyageur': commandes_voyageur,
        'commandes_client': commandes_client
    })
