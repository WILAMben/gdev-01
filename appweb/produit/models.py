from django.db import models
from utilisateur.models import User


# Create your models here.


class Produit(models.Model):
    reference_produit = models.CharField(max_length=250)
    nom_produit = models.CharField(max_length=250,null=True, blank=False)
    categorie_produit = models.CharField(max_length=250,null=True)
    niveau = models.CharField(max_length=250,null=True)

    date_ajout_produit =  models.DateTimeField(auto_now_add=True ,auto_now=False)
    date_update_produit = models.DateTimeField(auto_now_add=False, auto_now=True)

    nom_produit_ar = models.CharField(max_length=250,null=True)
    description_produit = models.TextField(null=True)
    description_produit_ar = models.TextField(null=True)
    prix_produit = models.DecimalField(decimal_places=2,max_digits=100,default=0.00, blank=True, null=True)
    active = models.BooleanField(default=True)
    notice = models.FileField(upload_to='produit/notice/',null=True, blank=True)


    def __unicode__(self):
        return "le produit: "+self.nom_produit +". la reference:  "+ self.reference_produit


class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit,on_delete="cascade")
    image = models.ImageField(upload_to='produit/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    date_update = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "le produit: " + self.Produit.nom_produit



class ProduitsFavorite(models.Model):
    class Meta:
         unique_together = (('id_user', 'id_produit'),)

    id_user = models.ForeignKey(User,on_delete="cascade")
    id_produit = models.ForeignKey(Produit,on_delete="cascade")