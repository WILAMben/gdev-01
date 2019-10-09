from django.urls import path, re_path, include

from produit import views as views



app_name= 'publication'

urlpatterns = [
       path('', views.hom, name='hom'),
    ]