from django.urls import path, re_path, include
from . import views


app_name= 'point_de_vente'

urlpatterns = [
       path('', views.point_view, name='point_view'),
       path('home/', views.venteHome, name='venteHome'),
       path('commande/', views.commandeView, name='commandeView'),
       path('traitement/', views.traitementView, name='traitementView'),
       path('historique/', views.historiqueView, name='historiqueView'),
       path('ChartBcBlVent', views.ChartBcBlVent, name='ChartBcBlVentsnap'),
       path('logout', views.logout, name='logout'),

]
