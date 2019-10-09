from gc import get_objects

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views import generic

from commande.models import Ligne_commande
from publication.models import Pub, Blog, ImageVente
from .models import Produit, ProduitsFavorite
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import auth, messages
from utilisateur.models import User
from django.db.models import Count

def changeLang(request):
    if request.session['lang'] == 'ar':
        request.session['lang'] = 'fr'
    else:
       request.session['lang'] = 'ar'
    return HttpResponseRedirect('/produit/')



def hom (request):
    return HttpResponseRedirect('/produit/')


def homy (request):
    return HttpResponseRedirect('/produit/')


def indexView(request):
    if 'comp1' not in request.session:
        request.session['comp1'] = 0
        request.session['comp2'] = 0
        request.session['comp3'] = 0
    

    
    
    if 'idUserBachNsegemUpdate' not in request.session:
            request.session['idUserBachNsegemUpdate'] = request.user.id
    
    #nseyyi ta3 3arbiya b session
    if 'lang' not in request.session:
        request.session['lang'] = 'ar'



    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))







    random=Produit.objects.filter(active=True).order_by('?')[:10]



    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
            les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))



    #hadi ta3 slide
    
    all = Produit.objects.filter(active=True)
    date_ajout = Produit.objects.filter(active=True).order_by('-id')
    template_name = 'produit/Home.html'
    context = {

        'all': all,
        'date_ajout': date_ajout,
        'les_plus_acheter': les_plus_acheter,
        
        'random':random,
        'p':p,
        'slide': Pub.objects.all(),
        'blog':Blog.objects.filter(type="blog").order_by('-id'),
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
        'imgvente':ImageVente.objects.filter(type="vente"),

    }
    return render(request, template_name, context)


def detailView(request, pk):
    if 'comp1' not in request.session:
        request.session['comp1'] = 0
        request.session['comp2'] = 0
        request.session['comp3'] = 0
   
    all = Produit.objects.filter(id=pk)
    a = Produit.objects.get(id=pk)
    catigo = a.categorie_produit
    cat = Produit.objects.filter(Q(categorie_produit=catigo) & Q(active=True) )
    template_name = 'produit/detail.html'
    context = {

        'all': all,
        'cat': cat,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
    }
    return render(request, template_name, context)






def recherchePro(request):
    try:
        ser = request.GET['ser']
        cat = request.GET['cat']
    except:
        ser = None
    if ser:


        contact_list = Produit.objects.filter((Q(reference_produit=ser) | Q(nom_produit=ser)| Q(nom_produit_ar=ser)| Q(niveau=ser))& Q(active=True)   )
        paginator = Paginator(contact_list, 4)  # Show 25 contacts per page
        template_name = 'produit/Recherche.html'
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        
        les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
        les_plus_acheter=[]
        for i in les_plus:
            if i.id_produit.active:
                  les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))
        
        p = []
        if 'comp1'  in request.session:
            if request.session['comp1'] != 0:
               p.append(Produit.objects.get(id=request.session['comp1']))
            if request.session['comp2'] != 0:
               p.append(Produit.objects.get(id=request.session['comp2']))
            if request.session['comp3'] != 0:
               p.append(Produit.objects.get(id=request.session['comp3']))







        context = {
            'p':p,
            'contacts': contacts,
            'hass': ser,
            'slide': Pub.objects.all(),
            'blog':Blog.objects.filter(type="blog"),
            'les_plus_acheter':les_plus_acheter,
            'imgCata':ImageVente.objects.filter(type="cataImg"),
        }

        return render(request, template_name, context)

    return HttpResponse("<h1>mamchatch recherch</h1>")


def rechCatigo(request):

    data = request.GET.get('ser')
    # had data howa parametre li trechercher bih 3la catigorie li rak 7abha
    all = Produit.objects.filter(Q(categorie_produit=data)& Q(active=True) )
    paginator = Paginator(all, 4)
    page = request.GET.get('page')

    all = paginator.get_page(page)
    template_name = 'produit/Recherche.html'
        
    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:

              les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))

    
    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))





    context = {
        'p':p,
        'contacts': all,
        'hass': data,
        'slide': Pub.objects.all(),
        'blog':Blog.objects.filter(type="blog"),
        'les_plus_acheter':les_plus_acheter,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
    }
    return render(request, template_name, context)


def rechCatigoSplit(request):
  anis = request.GET.get('ser')
  if anis== 'zafikor':
            all = Produit.objects.filter(active=True)
            paginator = Paginator(all, 9)
            page = request.GET.get('page')

            all = paginator.get_page(page)
            template_name = 'produit/Recherche.html'
        
            les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
            les_plus_acheter=[]
            for i in les_plus:
                if i.id_produit.active:
                     les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))

                     
            p = []
            if 'comp1'  in request.session:
                if request.session['comp1'] != 0:
                    p.append(Produit.objects.get(id=request.session['comp1']))
                if request.session['comp2'] != 0:
                    p.append(Produit.objects.get(id=request.session['comp2']))
                if request.session['comp3'] != 0:
                    p.append(Produit.objects.get(id=request.session['comp3']))





            context = {
                'p':p,
                'contacts': all,
                'hass': anis,
                'slide': Pub.objects.all(),
                'blog':Blog.objects.filter(type="blog"),
                'les_plus_acheter':les_plus_acheter,
                'imgCata':ImageVente.objects.filter(type="cataImg"),
            }
            return render(request, template_name, context)
  else:
    row = anis.split(",")

    all = Produit.objects.filter(Q(categorie_produit=row[1])& Q(active=True))
    for i in row:
        all = all | Produit.objects.filter(Q(categorie_produit=i)    & Q(active=True))

    paginator = Paginator(all, 4)
    page = request.GET.get('page')
    all = paginator.get_page(page)
    template_name = 'produit/Recherche.html'
        
    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
              les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))

    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))




    context = {
        'contacts': all,
        'hass': anis,
        'p':p,
        'slide': Pub.objects.all(),
        'blog':Blog.objects.filter(type="blog"),
        'les_plus_acheter':les_plus_acheter,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
    }
    return render(request, template_name, context)


def printPdf(request, pk):
    if request.method == 'POST':
        all = Produit.objects.filter(id=pk)

        template_name = 'produit/printPdf.html'
        context = {
            'all': all,
        }
        return render(request, template_name, context)


def addWish(request):
    if request.method == 'POST':
        id_produit = request.POST['id_produit']
        id_user = request.POST['id_user']

        us = User.objects.get(id=id_user)
        prodna = Produit.objects.get(id=id_produit)
        ProduitsFavorite.objects.create(
            id_user=us,
            id_produit=prodna,
        )
        return HttpResponse("<h1> mchat </h1>")
    return HttpResponse("<h1>hkjhkjhkjhkjkjgkjhgjkhjkhkjhkjhkjnbs</h1>")


def affichWish(request):
    idu =  request.session['idUserBachNsegemUpdate']
    user_sd = User.objects.get(id=idu)
    all = ProduitsFavorite.objects.filter(id_user=user_sd)
    paginator = Paginator(all, 4)
    page = request.GET.get('page')

    all = paginator.get_page(page)
    template_name = 'produit/favoris.html'
    
    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))



    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
            les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))


    context = {
        'p':p,
        'all': all,
        
        'slide': Pub.objects.all(),
        'les_plus_acheter': les_plus_acheter,
        'hass': idu,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
    }
    return render(request, template_name, context)


def suppWish(request):
    if request.method == 'POST':
        id_produit = request.POST['id_produit']
        id_user = request.POST['id_user']
        ProduitsFavorite.objects.filter(id_user=id_user, id_produit=id_produit).delete()
        return HttpResponseRedirect('/produit/wish/affich/' )
    return HttpResponse("mamchatch ta3 tmodifier qntt")



def addCompare(request):
    if request.method == 'POST':
        id_produit = request.POST['id_produit']
        if request.session['comp1'] == 0:
            request.session['comp1'] = id_produit
        elif request.session['comp2'] == 0:
            request.session['comp2'] = id_produit
        elif request.session['comp3'] == 0:
            request.session['comp3'] = id_produit
        return HttpResponse("makach plasa")
    return HttpResponse("ajoutah")

def affichCompare(request):
    p = []

    if request.session['comp1'] != 0:
        p.append(Produit.objects.get(id=request.session['comp1']))
    if request.session['comp2'] != 0:
        p.append(Produit.objects.get(id=request.session['comp2']))
    if request.session['comp3'] != 0:
        p.append(Produit.objects.get(id=request.session['comp3']))


    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
            les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))

    template_name = 'produit/compare.html'
    context = {
        'p': p,
        'les_plus_acheter': les_plus_acheter,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),

    }
    return render(request, template_name, context)

def suppCompare(request):
    cmp= request.GET.get('cmp')
    if request.session['comp1'] == cmp:
        request.session['comp1']= 0
    if request.session['comp2'] == cmp:
        request.session['comp2'] = 0
    if request.session['comp3'] == cmp:
        request.session['comp3'] = 0
    p = []

    if request.session['comp1'] != 0:
        p.append(Produit.objects.get(id=request.session['comp1']))
    if request.session['comp2'] != 0:
        p.append(Produit.objects.get(id=request.session['comp2']))
    if request.session['comp3'] != 0:
        p.append(Produit.objects.get(id=request.session['comp3']))

    template_name = 'produit/compare.html'
    context = {
        'p': p,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),

    }
    return render(request, template_name, context)

def contact(request):
    template_name = 'produit/contact.html'
    
    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))



    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
            les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))



    return render(request, template_name,{
        'p':p,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
        'les_plus_acheter': les_plus_acheter,
        
        'slide': Pub.objects.all(),})

def information(request):
    template_name = 'produit/information.html'
    
    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))




    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
            les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))


    return render(request, template_name, {'p':p,
        'text':Blog.objects.filter(type="nousSomme"),
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
        'les_plus_acheter': les_plus_acheter,
        
        'slide': Pub.objects.all(),})



def blog(request):
    template_name = 'produit/blog.html'
    all = Blog.objects.filter(type="blog")
    paginator = Paginator(all, 6)
    page = request.GET.get('page')

    all = paginator.get_page(page)
    
    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))




    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
            les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))

    context={
        'p':p,
        'touss':all,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
        'les_plus_acheter': les_plus_acheter,
        'slide': Pub.objects.all(),
    }

    return render(request, template_name, context)



def blog_post(request):
    id = request.GET.get('bbg')
    b = Blog.objects.filter(id=id)
    template_name = 'produit/blog_post.html'
    
    p = []
    if 'comp1'  in request.session:
       if request.session['comp1'] != 0:
          p.append(Produit.objects.get(id=request.session['comp1']))
       if request.session['comp2'] != 0:
          p.append(Produit.objects.get(id=request.session['comp2']))
       if request.session['comp3'] != 0:
          p.append(Produit.objects.get(id=request.session['comp3']))



    les_plus = Ligne_commande.objects.filter().annotate(num=Count('id_produit')).order_by('-num')[:10]
    les_plus_acheter=[]
    for i in les_plus:
        if i.id_produit.active:
            les_plus_acheter.append(Produit.objects.get(id=str(i.id_produit.id)))



    return render(request, template_name,{'p':p,
        'all':b,
        'imgCata':ImageVente.objects.filter(type="cataImg"),
        'pdfCata':ImageVente.objects.filter(type="cataPdf"),
        'les_plus_acheter': les_plus_acheter,
        'slide': Pub.objects.all(),})
