from django.urls import path, re_path
from . import views as main_views
from commande import views as commande_views


app_name= 'panier'

urlpatterns = [
    path('', main_views.affichPan, name='affichPan'),
    path('modif/', main_views.modifQntt, name='modifQntt'),
    path('suppPro/', main_views.suppPro, name='suppPro'),
    path('commander/', commande_views.ajouCommand, name='ajouCommand'),


]