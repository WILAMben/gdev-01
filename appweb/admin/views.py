
from django.contrib import messages, auth
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import os
from django.conf import settings

from panier.models import Panier_user
from utilisateur.models import User
from django.db.models import Count
from appweb.settings import MEDIA_URL, MEDIA_ROOT
from commande.models import Commande, Ligne_commande
from produit.models import Produit, ImageProduit, ProduitsFavorite
import datetime
import random
def logAdmin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.type != "admin":
                messages.success(request, 'nta machi admin')
                auth.logout(request)
                return HttpResponseRedirect('/admin_site/')

            else:
                auth.login(request, user)
                messages.success(request, 'rak mconicti')
                return HttpResponseRedirect('/admin_site/home/')



        else:
            if 'nbra' not in request.session:
                request.session['nbra'] =0

            request.session['nbra']=request.session['nbra']+1
            if request.session['nbra'] > 3 :
                request.session['trya']='non'
            messages.success(request, 'Email ou MDP incorrect svp ressayer')
            return HttpResponseRedirect('/admin_site/')


    template_name = 'admin/adminLog.html'
    return render(request, template_name)


def home_admin(request):
    if request.user.is_authenticated and request.user.type == "admin":
       template = 'admin/admin_page.html'
       context = {
          'tout': Produit.objects.all(),
          'vente':User.objects.filter(type="vente"),
       }
       return render(request, template, context)
    else:
        return HttpResponseRedirect('/admin_site/')

























def ajoutProd(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        reference_produit = request.POST.get('reference_produit')
        nom_produit = request.POST.get('nom_produit')
        nom_produit_ar = request.POST.get('nom_produit_ar')
        description_produit = request.POST.get('description_produit')
        description_produit_ar = request.POST.get('description_produit_ar')
        categorie_produit = request.POST.get('categorie')
        niveau = request.POST.get('niveau')
        #prix_produit = request.POST.get('prix_produit')

        
        if Produit.objects.filter(reference_produit=reference_produit).exists():
                    messages.error(request, "reference taken")
                    return HttpResponseRedirect("/admin_site/ajoutProd/")
     


        cree= Produit.objects.create(reference_produit=reference_produit, nom_produit=nom_produit,
                               nom_produit_ar=nom_produit_ar, description_produit=description_produit,
                               description_produit_ar=description_produit_ar, categorie_produit=categorie_produit,
                               niveau=niveau
                                )
    

        if 'upload' in request.FILES:
            r = request.FILES['upload']
            archivo=Produit.objects.get(id=cree.id)
            archivo.notice = r
            archivo.save(update_fields=['notice'])

            
            #cree.update(notice=r)


        if 'prix_produit' in request.POST:
            if request.POST.get('prix_produit') != ''  :
                
                  prix_produit = request.POST.get('prix_produit')
                 
                  archivo=Produit.objects.get(id=cree.id)
                  
        
                  archivo.prix_produit = prix_produit
                  archivo.save(update_fields=['prix_produit'])
            
        

        # hna najoutiw teswira l produit hada
        for f in request.FILES.getlist('file'):
            pr = Produit.objects.get(reference_produit=reference_produit, nom_produit=nom_produit)
            py = ImageProduit.objects.create(produit=pr, image=f)
            py.save()

        return HttpResponseRedirect('/admin_site/ajoutProd/')

    template = 'admin/ajoutProd.html'

    context = {
        'tout': Produit.objects.all(),
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template, context)


# modifier un produit +++++++++++++++++++++++++++++++++++++

#suprimmer prod
def modifierProd(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        id = request.POST['id']
        p = Produit.objects.get(id=id)

        if ProduitsFavorite.objects.filter(id_produit=p).exists():
            lap = ProduitsFavorite.objects.filter(id_produit=p)
            for item in lap:
                m = ProduitsFavorite.objects.get(id=item.id)
                ProduitsFavorite.delete(m)

        if Panier_user.objects.filter(id_panier_produit=p).exists():
            lap = Panier_user.objects.filter(id_panier_produit=p)
            for item_panier in lap:
                m = Panier_user.objects.get(id=item_panier.id)
                Panier_user.delete(m)

        if Ligne_commande.objects.filter(id_produit=p).exists():

            key = ''
            g = random.randint(15, 20)
            while len(key) < g:
                n = random.randint(0, 9)
                key += str(n)

            r = ImageProduit.objects.filter(produit=p.id)
            for y in r:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + y.image.url))
                y.delete()




            if p.notice:
                 os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + p.notice.url))

            Produit.objects.filter(id=id).update(active=False,reference_produit=key, notice=False)
            template = 'admin/modifierProd.html'
            context = {
                'all': Produit.objects.filter(active=True),
                'vente': User.objects.filter(type="vente"),

            }
            return render(request, template, context)

        r = ImageProduit.objects.filter(produit=p.id)
        if p.notice:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + p.notice.url))
        for y in r:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + y.image.url))
            y.delete()
        Produit.objects.filter(id=id).delete()

    template = 'admin/modifierProd.html'
    context = {
        'all': Produit.objects.filter(active=True),
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template, context)


def updatePr(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        produit_id = request.POST['id_ppr']
        all = Produit.objects.filter(id=produit_id)

        template_name = 'admin/updateProduct.html'
        context = {
            'all': all,
            'vente':User.objects.filter(type="vente"),
        }
        return render(request, template_name, context)
    return HttpResponse("mamchatch lpost")


def updatere(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':

        idff = request.POST['idFF']

        if 'upload' in request.FILES:
            r=request.FILES['upload']
            #Produit.objects.get(id=idff).update(notice=r)
            archivo = Produit.objects.get(id=idff)
            archivo.notice = r
            archivo.save(update_fields=['notice'])







        if (request.POST.get('reference_produit')):
            reference_produit = request.POST.get('reference_produit')
        else:
            reference_produit = request.POST.get('reference_produit1')











            
        if (request.POST.get('nom_produit')):
            nom_produit = request.POST.get('nom_produit')
        else:
            nom_produit = request.POST.get('nom_produit1')
        if (request.POST.get('nom_produit_ar')):
            nom_produit_ar = request.POST.get('nom_produit_ar')
        else:
            nom_produit_ar = request.POST.get('nom_produit_ar1')

        description_produit = request.POST.get('description_produit')
        description_produit_ar = request.POST.get('description_produit_ar')
        categorie_produit = request.POST.get('categorie')
        if (request.POST.get('niveau')):
            niveau = request.POST.get('niveau')
        else:
            niveau = request.POST.get('niveau1')
        if (request.POST.get('prix_produit')):
            prix_produit = request.POST.get('prix_produit')
        else:
            prix_produit = request.POST.get('prix_produit1')

        Produit.objects.filter(id=idff).update(  reference_produit=reference_produit, nom_produit=nom_produit,
                                               nom_produit_ar=nom_produit_ar, description_produit=description_produit,
                                               description_produit_ar=description_produit_ar,
                                               categorie_produit=categorie_produit,
                                               niveau=niveau, prix_produit=prix_produit)

        for f in request.FILES.getlist('file'):
            pr = Produit.objects.get(reference_produit=reference_produit, nom_produit=nom_produit)
            

            py = ImageProduit.objects.create(produit=pr, image=f)
            py.save()




        return HttpResponseRedirect('/admin_site/modifierProd/')





def photosEditt(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        id = request.POST['id_img']
        ob = ImageProduit.objects.get(id=id)
        os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + ob.image.url))
        ImageProduit.objects.filter(id=id).delete()
        produit_id = request.POST['id_ppr']
        all = Produit.objects.filter(id=produit_id)

        template_name = 'admin/updateProduct.html'
        context = {
            'all': all,
            'vente': User.objects.filter(type="vente"),
        }
        return render(request, template_name, context)


def photosEdit(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        id = request.POST['id_img']
        ob = ImageProduit.objects.get(id=id)
        os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + ob.image.url))
        ImageProduit.objects.filter(id=id).delete()
    template = 'admin/photosEdit.html'

    context = {
        'all': Produit.objects.all(),
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template, context)


def BcBl(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    today = datetime.datetime.now()
    List= []#commande avec success
    li = []#commande annuler
    template = 'admin/bcblChart.html'

    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-02-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year - 1) + "-12-31T13:20:30+03:00")).count())

    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-03-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-01-31T13:20:30+03:00")).count())

    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-04-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-02-28T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-05-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-03-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-06-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-04-30T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-07-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-05-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-08-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-06-30T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-09-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-07-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-10-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-08-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-11-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-09-30T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-12-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-10-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year + 1) + "-01-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-11-30T13:20:30+03:00")).count())
    #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-02-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year - 1) + "-12-31T13:20:30+03:00")).count())

    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-03-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-01-31T13:20:30+03:00")).count())

    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-04-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-02-28T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-05-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-03-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-06-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-04-30T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-07-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-05-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-08-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-06-30T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-09-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-07-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-10-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-08-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-11-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-09-30T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-12-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-10-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year + 1) + "-01-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-11-30T13:20:30+03:00")).count())





    context = {
        'bc': List,
        'bAnu':li,
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template, context)


def BcBlVent(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    idu = request.GET.get('vnt')
    vnt_obj = User.objects.get(id=idu)
    name=vnt_obj.username
    today = datetime.datetime.now()
    List= []#commande avec success
    li = []#commande annuler
    template = 'admin/bcblChartVente.html'

    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-02-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year - 1) + "-12-31T13:20:30+03:00")).count())

    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-03-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-01-31T13:20:30+03:00")).count())

    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-04-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-02-28T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-05-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-03-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-06-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-04-30T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-07-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-05-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-08-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-06-30T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-09-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-07-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-10-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-08-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-11-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-09-30T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year) + "-12-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-10-31T13:20:30+03:00")).count())
    List.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=False) & Q(
        date_commande__lte=str(today.year + 1) + "-01-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-11-30T13:20:30+03:00")).count())
    #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-02-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year - 1) + "-12-31T13:20:30+03:00")).count())

    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-03-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-01-31T13:20:30+03:00")).count())

    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-04-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-02-28T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-05-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-03-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-06-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-04-30T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-07-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-05-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-08-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-06-30T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-09-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-07-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-10-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-08-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-11-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-09-30T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year) + "-12-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-10-31T13:20:30+03:00")).count())
    li.append(Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_archive=True) & Q(annulation_levraison=True) & Q(
        date_commande__lte=str(today.year + 1) + "-01-01T13:20:30+03:00") & Q(
        date_commande__gte=str(today.year) + "-11-30T13:20:30+03:00")).count())


    context = {
        'bc': List,
        'bAnu':li,
        'vente':User.objects.filter(type="vente"),
        'name':name,
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template, context)


def historiqueCmd(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    idu = request.GET.get('vnt')
    vnt_obj = User.objects.get(id=idu)
    name=vnt_obj.username
    all = Commande.objects.filter(Q(id_point_vente=vnt_obj) & Q(etat_commande=True) & Q(etat_archive=True))

    context = {
        'all': all,
        'name':name,
        'vente':User.objects.filter(type="vente"),

    }
    template_name = 'admin/historique_admin_vente.html'
    return render(request, template_name, context)

def ajouPointVente(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password"]

        nom = request.POST["name"]

        tlf = request.POST["tlf"]
        maps = request.POST["maps"]
        adresse = request.POST["adresse"]
        wilaya = request.POST["wilaya"]
        fax=""
        portable=""
        if 'fax' in request.POST:
            fax = request.POST["fax"]
        if 'portable' in request.POST:
            portable = request.POST["portable"]
        if User.objects.filter(username=username).exists():
                    messages.error(request, "username taken")
                    template_name = 'admin/ajouPointVente.html'
                    return HttpResponseRedirect('/admin_site/ajouPointVente/')

        else:

                    if User.objects.filter(email=email).exists():
                        messages.error(request, "email taken")
                        template_name = 'admin/ajouPointVente.html'
                        return HttpResponseRedirect('/admin_site/ajouPointVente/')

                    else:
                        user= User.objects.create_user(username=username,email=email,password=password1,wilaya_user=wilaya, type="vente",
                                                       first_name=nom,rc=maps,adresse_user=adresse,telephone_user=tlf,confirmed=True,fax_user=fax,telephone_portable_user=portable)
                     

                        template_name = 'admin/ajouPointVente.html'
                        context = {

                            'vente': User.objects.filter(type="vente"),

                        }
                        return render(request, template_name, context)

    template_name = 'admin/ajouPointVente.html'
    context = {

        'vente': User.objects.filter(type="vente"),

    }
    return render(request, template_name, context)







def chart_js(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    today = datetime.datetime.now()
    jan= User.objects.filter(Q(date_joined__lte= str(today.year)+"-02-01T13:20:30+03:00")& Q(date_joined__gte=str(today.year -1) +"-12-31T13:20:30+03:00")).count()

    feb = User.objects.filter(Q(date_joined__lte=str(today.year) + "-03-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-01-31T13:20:30+03:00")).count()

    mar = User.objects.filter(Q(date_joined__lte=str(today.year) + "-04-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-02-28T13:20:30+03:00")).count()
    avr = User.objects.filter(Q(date_joined__lte=str(today.year) + "-05-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-03-31T13:20:30+03:00")).count()
    mai = User.objects.filter(Q(date_joined__lte=str(today.year) + "-06-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-04-30T13:20:30+03:00")).count()
    jun = User.objects.filter(Q(date_joined__lte=str(today.year) + "-07-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-05-31T13:20:30+03:00")).count()
    jul = User.objects.filter(Q(date_joined__lte=str(today.year) + "-08-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-06-30T13:20:30+03:00")).count()
    aut = User.objects.filter(Q(date_joined__lte=str(today.year) + "-09-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-07-31T13:20:30+03:00")).count()
    sep = User.objects.filter(Q(date_joined__lte=str(today.year) + "-10-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-08-31T13:20:30+03:00")).count()
    oct = User.objects.filter(Q(date_joined__lte=str(today.year) + "-11-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-09-30T13:20:30+03:00")).count()
    nvb = User.objects.filter(Q(date_joined__lte=str(today.year) + "-12-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-10-31T13:20:30+03:00")).count()
    dec = User.objects.filter(Q(date_joined__lte=str(today.year+1) + "-01-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-11-30T13:20:30+03:00")).count()
    jan1= User.objects.filter(Q(date_joined__lte= str(today.year)+"-02-01T13:20:30+03:00")&
        Q(date_joined__gte=str(today.year -1) +"-12-31T13:20:30+03:00")& Q(confirmed=True)).count()

    feb1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-03-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-01-31T13:20:30+03:00")& Q(confirmed=True)).count()

    mar1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-04-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-02-28T13:20:30+03:00")& Q(confirmed=True)).count()
    avr1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-05-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-03-31T13:20:30+03:00")& Q(confirmed=True)).count()
    mai1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-06-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-04-30T13:20:30+03:00")& Q(confirmed=True)).count()
    jun1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-07-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-05-31T13:20:30+03:00")& Q(confirmed=True)).count()
    jul1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-08-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-06-30T13:20:30+03:00")& Q(confirmed=True)).count()
    aut1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-09-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-07-31T13:20:30+03:00")& Q(confirmed=True)).count()
    sep1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-10-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-08-31T13:20:30+03:00")& Q(confirmed=True)).count()
    oct1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-11-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-09-30T13:20:30+03:00")& Q(confirmed=True)).count()
    nvb1 = User.objects.filter(Q(date_joined__lte=str(today.year) + "-12-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-10-31T13:20:30+03:00")& Q(confirmed=True)).count()
    dec1 = User.objects.filter(Q(date_joined__lte=str(today.year+1) + "-01-01T13:20:30+03:00") & Q(
        date_joined__gte=str(today.year) + "-11-30T13:20:30+03:00")& Q(confirmed=True)).count()


    context = {
        'jan':jan,
        'feb': feb,
        'mar': mar,
        'avr': avr,
        'mai': mai,
        'jun': jun,
        'jul': jul,
        'aut': aut,
        'sep': sep,
        'oct': oct,
        'nvb': nvb,
        'dec': dec,
        'jan': jan,
        'jan1': jan1,
        'feb1': feb1,
        'mar1': mar1,
        'avr1': avr1,
        'mai1': mai1,
        'jun1': jun1,
        'jul1': jul1,
        'aut1': aut1,
        'sep1': sep1,
        'oct1': oct1,
        'nvb1': nvb1,
        'dec1': dec1,
        'jan1': jan1,
        'vente':User.objects.filter(type="vente"),
    }
    template_name = 'admin/chart_js.html'
    return render(request, template_name,context)




def bloquer(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        id = request.POST["id"]
        

        vn = User.objects.get(id=id)
        if vn.confirmed:
            vnt = request.POST['pet_select']
            User.objects.filter(id=id).update(confirmed=False)
            vntnow= User.objects.get(id=id)
            vntnw= User.objects.get(id=vnt)

            com = Commande.objects.filter(Q(etat_archive=False) & Q(id_point_vente=vntnow) )
            for c in com:
                Commande.objects.filter(id=c.id).update(id_point_vente=vntnw)



        else:
            User.objects.filter(id=id).update(confirmed=True)
        template_name = 'admin/bloquer_debloquer.html'
        context = {
             'vnt':User.objects.filter(id=id),

             'vente': User.objects.filter(type="vente"),
        }
        return render(request, template_name,context)

    else:
        idu = request.GET.get('vnt')
        template_name = 'admin/bloquer_debloquer.html'
        context = {
             'vnt':User.objects.filter(id=idu),

             'vente': User.objects.filter(type="vente"),
        }
        return render(request, template_name,context)


def chart_wilaya(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')


    les_plus=[]
    num=0
    wila = User.objects.values('wilaya_user').annotate(num=Count('wilaya_user')).order_by('-num')[:5]
    for i in wila:
        r = []
        r.append(i['wilaya_user'])
        r.append(i['num'])
        num=num+i['num']

        les_plus.append(r)
    r = []
    r.append('autre')
    r.append(User.objects.all().count() - num)
    les_plus.append(r)



    template_name = 'admin/chart_wilaya.html'
    context={
        'wilaya':les_plus,
        'vente':User.objects.filter(type="vente"),
    }
    return render(request, template_name,context)



def logout(request):

        auth.logout(request)
        return HttpResponseRedirect('/admin_site/')

def impLev(request):

    if request.method == 'POST':
        id_com = request.POST['commid']
        awm = Commande.objects.filter(id=id_com)
        template_name = 'admin/imprimerLev.html'
        context = {
            'com': awm,

        }
        return render(request, template_name, context)


def deplasser(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')

    if request.method == 'POST':
        id_com = request.POST['commid']
        vnt = request.POST['pet_select']
        v = User.objects.get(id=vnt)
        Commande.objects.filter(id=id_com).update(id_point_vente=v)

    all = Commande.objects.filter(etat_archive=False)

    context = {
        'all': all,

        'vente': User.objects.filter(type="vente"),

    }
    template_name = 'admin/deplasserCommande.html'
    return render(request, template_name, context)



def Type_client(request):

    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')


    dir=User.objects.filter(type_sp="directeur").count()
    enseignant=User.objects.filter(type_sp="enseignant").count()
    etudiant=User.objects.filter(type_sp="etudiant").count()
    laborantin=User.objects.filter(type_sp="laborantin").count()
    intendant=User.objects.filter(type_sp="intendant").count()
    revendeur=User.objects.filter(type_sp="revendeur").count()
    vente=User.objects.filter(type="vente").count()
    context = {
        'dir': dir,
        'enseignant': enseignant,
        'etudiant': etudiant,
        'laborantin': laborantin,
        'intendant': intendant,
        'revendeur': revendeur,
        'vent': vente,

        'vente': User.objects.filter(type="vente"),

    }
    template_name = 'admin/Type_client.html'
    return render(request, template_name, context)

