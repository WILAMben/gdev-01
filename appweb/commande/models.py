from django.db import models

from produit.models import Produit
from utilisateur.models import User

class Commande(models.Model):
    etat_commande = models.BooleanField(default=False)
    etat_archive = models.BooleanField(default=False)
    annulation_levraison= models.BooleanField(default=False)
    note_dannulation= models.CharField(max_length=250,default=" ",blank=True)
    bon_de_commande = models.CharField(max_length=250,blank=True)
    bon_de_livraison = models.ImageField(upload_to='commande/images/',blank=True)
    date_commande = models.DateTimeField(blank=True)
    date_levraison =models.DateTimeField(blank=True,null=True)
    id_user = models.ForeignKey(User, on_delete="cascade",  related_name='user')
    id_point_vente = models.ForeignKey(User, on_delete="cascade",  related_name='point_vente')


    def __str__(self):
        return "id de la commande: "+str(self.id)




class Ligne_commande(models.Model):
    class Meta:
         unique_together = (('id_commande', 'id_produit'),)

    id_commande = models.ForeignKey(Commande,on_delete="cascade")
    id_produit = models.ForeignKey(Produit,on_delete="cascade")
    quantite = models.IntegerField()


    def __str__(self):
        return "id de ligne de command: "+str(self.id)

