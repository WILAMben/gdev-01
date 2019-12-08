from django.urls import path, re_path
from . import views

app_name= 'utilisateur'

urlpatterns = [
         path('', views.login_view, name='login_view'),
         path('contactEmail/', views.contactEmail, name='contactEmail'),
         path('off/', views.lougout_view, name='lougout_view'),
         path('registre/', views.registre_view, name='registre_view'),
         path('registre/key/', views.keyRegistre_view, name='keyRegistre_view'),
         path('registre/key/rev', views.renvoyer_code, name='renvoyer_code'),
         path('mdpOublier/', views.mdpOublier, name='mdpOublier'),
         re_path(r'^activate/(?P<codeActivation>[0-9]+)/$', views.activation, name='activation'),
         #re_path(r'^activate/(?P<codeActivation>[0-9]+)/welcom/$', views.activated, name='activated'),
         re_path(r'^mdpInit/(?P<mdpInit>[0-9]+)/$', views.initmdp, name='initmdp'),
         #re_path(r'^mdpInit/(?P<mdpInit>[0-9]+)/finale/$', views.initmdpFinal, name='initmdpFinal'),
         re_path(r'^mdpInit/finale/$', views.initmdpFinal, name='initmdpFinal'),
         path('update_info/', views.update_info, name='update_info'),
         path('suppCompte/', views.suppCompte, name='suppCompte'),





]