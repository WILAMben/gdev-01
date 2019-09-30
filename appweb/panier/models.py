from django.db import models
from produit.models import Produit
from utilisateur.models import User




class Panier_user(models.Model):
    class Meta:
        unique_together = (('id_panier_user', 'id_panier_produit'),)

    id_panier_user = models.ForeignKey(User, on_delete="cascade")
    id_panier_produit = models.ForeignKey(Produit, on_delete="cascade")
    quantite_produit = models.IntegerField()
