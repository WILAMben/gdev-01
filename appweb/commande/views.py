from django.http import HttpResponse, HttpResponseRedirect
from gc import get_objects
import io
from django.http import FileResponse
from datetime import datetime
from django.contrib import auth
from commande.models import Commande, Ligne_commande
from panier.models import Panier_user
from publication.models import ImageVente

from produit.models import Produit
from utilisateur.models import User
from django.shortcuts import render

# Create your views here.
def ajouCommand(request):
    if request.method == 'POST':
        id_user = request.POST['id_user']
        id_vente = request.POST['id_vente']
        user_sd = User.objects.get(id=id_user)
        vente_sd = User.objects.get(id=id_vente)
        #lazem ndjib nhar ta3 lyom
        date=datetime.now()
        comm =  Commande.objects.create(

            date_commande =date,
            id_user =user_sd,
            id_point_vente =vente_sd,

        )
        comm.save()


        lap = Panier_user.objects.filter(id_panier_user=user_sd)
        for item_panier in lap:
            p = Produit.objects.get(id=item_panier.id_panier_produit.id)
            awm = Ligne_commande.objects.create(
                id_commande=comm,
                id_produit=p,
                quantite=item_panier.quantite_produit ,
            )
            awm.save()
            m=Panier_user.objects.get(id=item_panier.id)
            Panier_user.delete(m)




        return HttpResponseRedirect("/commande/?id="+str(id_user ))




def commandeViews(request):
    if 'comp1' not in request.session:
        request.session['comp1'] = 0
        request.session['comp2'] = 0
        request.session['comp3'] = 0
  
        
    idu = request.GET.get('id')
    akm= User.objects.get(id=idu)
    non_trt = Commande.objects.filter(id_user=akm,etat_commande=False,etat_archive=False)
    trt = Commande.objects.filter(id_user=akm,etat_commande=True,etat_archive=False)
    supp = Commande.objects.filter(id_user=akm,etat_archive=True,annulation_levraison=True)
    val = Commande.objects.filter(id_user=akm,etat_archive=True,annulation_levraison=False)
    template_name = 'commande/commandeViews.html'
    context = {
        'non_trt': non_trt,
        'trt': trt,
        'supp': supp,
        'val': val,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
    }
    return render(request, template_name, context)



def hassand(request):
    if request.method == 'POST':
        id_com = request.POST['commid']
        awm = Commande.objects.filter(id=id_com)
        akm=Commande.objects.get(id=id_com)
        all = Ligne_commande.objects.filter(id_commande=akm)
        totale=0
        for gaw in awm:
            for t in gaw.ligne_commande_set.all():
                totale=totale+ (t.quantite * t.id_produit.prix_produit)


        template_name = 'commande/commLove.html'
        context = {
            'all': all,
            'com':awm,
            'totale':totale,
        }
        return render(request, template_name, context)

    return HttpResponse("hhfhfhh")