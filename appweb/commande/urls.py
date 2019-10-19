from django.urls import path
from . import views

app_name= 'commande'

urlpatterns = [
         path('', views.commandeViews, name='commandeViews'),
         path('hass', views.hassand, name='hassand'),

]