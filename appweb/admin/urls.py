from django.urls import path, re_path
from . import views as views
from publication import  views as pub_views




app_name= 'admine'

urlpatterns = [
    path('', views.logAdmin, name='logAdmin'),
    path('home/', views.home_admin, name='home_admin'),
    path('ajoutProd/', views.ajoutProd, name='ajourProd'),
    path('modifierProd/', views.modifierProd, name='modifierProd'),
    path('modifierProd/update/', views.updatePr, name='updatePr'),
    path('modifierProd/update/up/', views.updatere, name='updatere'),

    path('photosEditt/', views.photosEditt, name='photosEditt'),
    path('photosEdit/', views.photosEdit, name='photosEdit'),



    path('addPub/', pub_views.addPub, name='addPub'),
    path('addPub2/', pub_views.addPub2, name='addPub2'),
    path('addBlog/', pub_views.addBlog, name='addBlog'),
    path('suppPub/', pub_views.suppPub, name='suppPub'),
    path('modifierQuiSommeNous/', pub_views.modifierQuiSommeNous, name='modifierQuiSommeNous'),
    path('imgPointeVente/', pub_views.imgPointeVente, name='imgPointeVente'),
    path('changerImgCata/', pub_views.changerImgCata, name='changerImgCata'),



    path('BcBl/', views.BcBl, name='BcBl'),
    path('BcBlVent', views.BcBlVent, name='BcBlVent'),
    path('chart_wilaya', views.chart_wilaya, name='chart_wilaya'),
    path('Type_client', views.Type_client, name='Type_client'),
    path('bloquer', views.bloquer, name='bloquer'),
    path('chart_js/', views.chart_js, name='chart_js'),
    path('historiqueCmd', views.historiqueCmd, name='historiqueCmd'),
    path('ajouPointVente/', views.ajouPointVente, name='ajouPointVente'),
    path('logout', views.logout, name='logout'),
    path('deplacer', views.deplasser, name='deplacer'),
    path('impLev', views.impLev, name='impLev'),


]
