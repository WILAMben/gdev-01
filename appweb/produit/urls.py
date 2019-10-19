from django.urls import path, re_path, include
from . import views as mais_views
from panier import views as panier_views
from utilisateur import views as utilisateur_views



app_name= 'produit'

urlpatterns = [
       path('', mais_views.indexView, name='index'),

       path('changeLang', mais_views.changeLang, name='changeLang'),

       re_path(r'^(?P<pk>[0-9]+)/$', mais_views.detailView, name='detail'),
       re_path(r'^(?P<pk>[0-9]+)/printPdf/$', mais_views.printPdf, name='printPdf'),
       path('recherche/', mais_views.recherchePro, name='recherchePro'),
       path('create/', panier_views.addPanier, name='addPanier'),
       path('wish/', mais_views.addWish, name='addWish'),
       path('wish/affich/', mais_views.affichWish, name='affichWish'),
       path('wish/supp/', mais_views.suppWish, name='suppWish'),
       path('compare/', mais_views.addCompare, name='addCompare'),
       path('compare/affich/', mais_views.affichCompare, name='affichCompare'),
       path('compare/affich/suup', mais_views.suppCompare, name='suppCompare'),
       path('login/', include('utilisateur.urls')),
       path('rechCatigo/', mais_views.rechCatigo, name='rechCatigo'),
       path('rechCatigoSplit/', mais_views.rechCatigoSplit, name='rechCatigoSplit'),
       path('contact', mais_views.contact, name='contact'),
       path('blog', mais_views.blog, name='blog'),
       path('blog_post', mais_views.blog_post, name='blog_post'),
       path('information', mais_views.information, name='information'),


]