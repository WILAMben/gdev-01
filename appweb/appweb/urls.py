"""appweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from produit import views as views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', include('publication.urls')),
    path('goldenDevAdminPanel/', admin.site.urls),
    path('produit/', include('produit.urls')),
    path('commande/', include('commande.urls')),
    path('utilisateur/', include('utilisateur.urls')),
    path('panier/', include('panier.urls')),
    path('point_vente/', include('point_de_vente.urls')),
    path('admin_site/', include('admin.urls')),
    
    #re_path(r'^(.*)/$',  views.homy, name='homy'),
    
    #re_path(r'^.*$',  views.homy, name='homy')
  

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)