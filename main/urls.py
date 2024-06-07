from django.urls import path, include  # Importer la fonction include
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'), # Add this line
    path('connexion/', views.connexion, name='connexion'),
    path('rechercher_commandes/', views.rechercher_commandes, name='rechercher_commandes'),
    path('creer_commande/<int:voyageur_id>/', views.creer_commande, name='creer_commande'),
    path('commande_details/<int:commande_id>/', views.commande_details, name='commande_details'),
    path('mes_commandes/', views.mes_commandes, name='mes_commandes'),
]