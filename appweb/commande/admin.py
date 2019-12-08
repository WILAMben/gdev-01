from django.contrib import admin

from .models import Commande, Ligne_commande

admin.site.register(Commande)
admin.site.register(Ligne_commande)