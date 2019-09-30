from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
# Create your views here.
from panier.models import Panier_user
from produit.models import Produit
from utilisateur.models import User

from publication.models import ImageVente


def addPanier(request):
    if request.method == 'POST':
        id_produit = request.POST['id_produit']
        id_user = request.POST['id_user']
        qntt = request.POST['qntt']
        us=     User.objects.get(id=id_user)
        prodna= Produit.objects.get(id=id_produit)

        
        if Panier_user.objects.filter(Q(id_panier_user=us) & Q(id_panier_produit=prodna)).exists():
            p=Panier_user.objects.get(Q(id_panier_user=us) & Q(id_panier_produit=prodna))
            Panier_user.objects.filter(Q(id_panier_user=us) & Q(id_panier_produit=prodna)).update(quantite_produit=p.quantite_produit+int(qntt))

        else:

            Panier_user.objects.create(
                id_panier_user=us,
                id_panier_produit=prodna,
                quantite_produit=qntt

            )
        return HttpResponse("<h1> mchat </h1>")
    return HttpResponse("<h1>hkjhkjhkjhkjkjgkjhgjkhjkhkjhkjhkjnbs</h1>")

def affichPan(request):
    idu= request.GET.get('id')
    user_sd = User.objects.get(id=idu)
    all = Panier_user.objects.filter(id_panier_user=user_sd)
    template_name = 'panier/panier.html'
    vente= User.objects.filter(type="vente")
    tot=0
    for p in all:
        if p.id_panier_produit.prix_produit == None:
            y = 0
        else:
            y= p.id_panier_produit.prix_produit
        tot=tot+ p.quantite_produit*y

    context = {
        'all': all,
        'vente':vente,
        'totale':tot,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
    }
    return render(request, template_name, context)


def modifQntt(request):
    if request.method == 'POST':
        id_panier = request.POST['id_panier']
        id_user = request.POST['id_user']
        qntt = request.POST['qtt']
        Panier_user.objects.filter(id=id_panier).update(quantite_produit=qntt)
        return  HttpResponseRedirect('/panier/?id='+id_user)
    return HttpResponse("mamchatch ta3 tmodifier qntt")


def suppPro(request):
    idd = request.GET.get('pan')
    id_user=request.GET.get('us')
    Panier_user.objects.get(id=idd).delete()
    return  HttpResponseRedirect('/panier/?id='+str(id_user))