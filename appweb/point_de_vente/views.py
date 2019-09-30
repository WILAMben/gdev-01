from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages, auth
from django.db.models import Q

from utilisateur.models import User
from datetime import datetime


# Create your views here.
from commande.models import Commande, Ligne_commande


def point_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.type != "vente":

                messages.success(request, 'nta machi point de vente')
                return HttpResponseRedirect('/point_vente/')


            elif user.confirmed == False:


                messages.success(request, 'non confirmer')
                auth.logout(request)
                return HttpResponseRedirect('/point_vente/')


            else:
                auth.login(request, user)
                messages.success(request, 'rak mconicti')
                return HttpResponseRedirect('/point_vente/home/')



        else:
            if 'nbrv' not in request.session:
                request.session['nbrv'] =0

            request.session['nbrv']=request.session['nbrv']+1
            if request.session['nbrv'] > 3 :
                request.session['tryv']='non'
            messages.success(request, 'Email ou MDP incorrect svp ressayer')
            return HttpResponseRedirect('/point_vente/')


    template_name = 'point_de_vente/point_vente.html'
    return render(request, template_name)



def venteHome(request):

    if not request.user.is_authenticated or request.user.type != "vente":
        return HttpResponseRedirect('/point_vente/')
    template_name = 'point_de_vente/point_vente_home.html'
    return render(request, template_name)


def commandeView(request):

    if not request.user.is_authenticated or request.user.type != "vente":
        return HttpResponseRedirect('/point_vente/')
    if request.user.is_authenticated and request.user.type == "vente" :

      if request.method == 'POST':
          id = request.POST['idCommande']


          if 'suprimer' in request.POST:
              cm=Commande.objects.get(id=id)
              cmp= Ligne_commande.objects.filter(id_commande=cm).count()
              for i in range(1, cmp+1):
                  Ligne_commande.objects.filter(id_commande=cm).delete()

              Commande.objects.filter(id=id).delete()

              all = Commande.objects.filter(Q(id_point_vente=request.user)& Q(etat_commande=False)& Q(etat_archive=False) )
              context = {
                      'all': all,
              }
              template_name = 'point_de_vente/commande_vente.html'
              return render(request, template_name, context)

          if 'valider' in request.POST:


              Commande.objects.filter(id=id).update(etat_commande=True)

              all = Commande.objects.filter(Q(id_point_vente=request.user)& Q(etat_commande=False)& Q(etat_archive=False) )
              context = {
                      'all': all,
              }
              template_name = 'point_de_vente/commande_vente.html'
              return render(request, template_name, context)

      else:

          all = Commande.objects.filter(Q(id_point_vente=request.user) & Q(etat_commande=False) & Q(etat_archive=False))

          context = {
              'all': all,

          }
          template_name = 'point_de_vente/commande_vente.html'
          return render(request, template_name, context)

    else:
        return HttpResponse('gjhgjhg')

def traitementView(request):

    if not request.user.is_authenticated or request.user.type != "vente":
        return HttpResponseRedirect('/point_vente/')
    if request.user.is_authenticated and request.user.type == "vente" :
        if request.method == 'POST':
            id = request.POST['idCommande']
            note = request.POST['note']
            fr = request.POST['validite']

            Commande.objects.filter(id=id).update(etat_archive=True)
            if  fr== "annuler":
                Commande.objects.filter(id=id).update(note_dannulation=note)
                Commande.objects.filter(id=id).update(annulation_levraison=True)
                date = datetime.now()
                Commande.objects.filter(id=id).update(date_levraison=date)
            else:
                Commande.objects.filter(id=id).update(annulation_levraison=False)
                filepath = request.FILES['bonlevrai']

                archivo = Commande.objects.get(id=id)
                archivo.bon_de_livraison = filepath
                archivo.save(update_fields=['bon_de_livraison'])




                #Commande.objects.filter(id=id).update(bon_de_livraison=filepath)
                date = datetime.now()
                Commande.objects.filter(id=id).update(date_levraison=date)
                Commande.objects.filter(id=id).update(note_dannulation=note)

            #if len(request.FILES) != 0:
             #   filepath = request.FILES['bonlevrai']
              #  Commande.objects.filter(id=id).update(bon_de_livraison=filepath)
               # date = datetime.now()
                #Commande.objects.filter(id=id).update(date_levraison=date)

            #note = request.POST['note']
            #if note !="":
             #   Commande.objects.filter(id=id).update(note_dannulation=note)
              #  Commande.objects.filter(id=id).update(annulation_levraison=True)




        all = Commande.objects.filter(Q(id_point_vente=request.user)& Q(etat_commande=True) & Q(etat_archive=False))
        context = {
            'all': all,
        }
        template_name = 'point_de_vente/traitement_vente.html'
        return render(request, template_name, context)

    return HttpResponseRedirect('/point_vente/')



def historiqueView(request):

    if not request.user.is_authenticated or request.user.type != "vente":
        return HttpResponseRedirect('/point_vente/')
    if request.user.is_authenticated and request.user.type == "vente" :
        if request.method == 'POST':
            id = request.POST['idCommande']
            Commande.objects.filter(id=id).update(etat_commande=True)

        all = Commande.objects.filter(Q(id_point_vente=request.user)& Q(etat_commande=True)& Q(etat_archive=True) )
        valider=Commande.objects.filter(Q(id_point_vente=request.user)& Q(etat_commande=True)& Q(etat_archive=True)& Q(annulation_levraison=False) )
        nonValider=Commande.objects.filter(Q(id_point_vente=request.user)& Q(etat_commande=True)& Q(annulation_levraison=True) )
        context = {
            'all': all,
            'valider':valider,
            'nonValider':nonValider,
        }
        template_name = 'point_de_vente/historique_vente.html'
        return render(request, template_name, context)

    else:
        return HttpResponseRedirect('/point_vente/')



def ChartBcBlVent(request):

    if not request.user.is_authenticated or request.user.type != "vente":
        return HttpResponseRedirect('/point_vente/')
    idu = request.GET.get('vnt')
    vnt_obj = User.objects.get(id=idu)
    name = vnt_obj.username
    today = datetime.now()
    List= []#commande avec success
    li = []#commande annuler
    template = 'point_de_vente/bcblChartVente.html'

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


def logout(request):

        auth.logout(request)
        return HttpResponseRedirect('/point_vente/')