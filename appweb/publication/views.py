from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from utilisateur.models import User
from publication.models import Pub, Blog, ImageVente

import os
from django.conf import settings

from appweb.settings import MEDIA_URL, MEDIA_ROOT


def addPub(request):
    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')
    if request.method == 'POST':
        image = request.FILES['image']
        t1=request.POST['t1']
        t2=request.POST['t2']
        Pub.objects.create(img=image,type="slide",titre1=t1,titre2=t2)

    template_name = 'admin/addSlide.html'
    context= {
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template_name,context)



def addPub2(request):
    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')
    if request.method == 'POST':
        image = request.FILES['image']
        t1=request.POST['t1']
        t2=request.POST['t2']
        Pub.objects.create(img=image,type="demi_slide",titre1=t1,titre2=t2)

    template_name = 'admin/addSlide2.html'
    context = {
        'vente': User.objects.filter(type="vente"),

    }
    return render(request, template_name,context)



def addBlog(request):
    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')
    if request.method == 'POST':
        image = request.FILES['image']
        t1=request.POST['t1']
        t2=request.POST['t2']
        Blog.objects.create(img=image,titre=t1,description=t2,type="blog")
    template_name = 'admin/addBlog.html'

    return render(request, template_name,{
        'vente':User.objects.filter(type="vente"),

    })

def suppPub(request):
    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')
    if 'suprimer' in request.POST:
        id = request.POST['id']
        ob=Pub.objects.get(id=id)
        
        os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + ob.img.url))
        Pub.objects.filter(id=id).delete()
    elif 'suprimerBlog' in request.POST:
        id = request.POST['id']
        ob=Blog.objects.get(id=id)
        
        os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + ob.img.url))
        Blog.objects.filter(id=id).delete()
        #Blog.objects.get(id=id).delete()


    template_name = 'admin/suppPub.html'
    context={
        'pub':Pub.objects.all(),
        'blog':Blog.objects.filter(type="blog"),
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template_name, context)





def modifierQuiSommeNous (request):
    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')
    if request.method == 'POST':

        t1=request.POST['descr']
        print("hhhhhhhhhhhhhhhhhhhhhhh")
        print(t1)
        print("jjjjjjjjjjjjjjj")


        Blog.objects.filter(type="nousSomme").delete()

        Blog.objects.create(description=t1,type="nousSomme")




    template_name = 'admin/modifierQuiSommeNous.html'
    context={
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template_name, context)


def imgPointeVente (request): 
    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')
    
    
    
    if 'ajouter' in request.POST:
        image = request.FILES['image']
        ImageVente.objects.create(img=image,type="vente")

    if 'suprimer' in request.POST:
        id = request.POST['id']
        ob=ImageVente.objects.get(id=id)
        os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + ob.img.url))
        ImageVente.objects.filter(id=id).delete()

    template_name = 'admin/imgPointeVente.html'
    context={
        'imgVT':ImageVente.objects.filter(type="vente"),
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template_name, context)

def changerImgCata(request):
    if not request.user.is_authenticated or request.user.type != "admin":
        return HttpResponseRedirect('/admin_site/')
    if request.method == 'POST':

        t1=request.FILES['image']
        t2=request.FILES['pdf']
        
        ob=ImageVente.objects.get(type="cataImg")
        os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + ob.img.url))

#doekdoekdoekdoekdoekdkeodkeod
# eidjeidjeidjejdiejdiejdiejd
# djeidjeidjiejdejdejdjeidjeid      
        obb=ImageVente.objects.get(type="cataPdf")
        os.remove(os.path.join(settings.MEDIA_ROOT, str(MEDIA_ROOT)[:-6] + obb.img.url))

        ImageVente.objects.filter(type="cataImg").delete()
        ImageVente.objects.filter(type="cataPdf").delete()

        ImageVente.objects.create(img=t1,type="cataImg")
        ImageVente.objects.create(img=t2,type="cataPdf")




    template_name = 'admin/changerImgCata.html'
    context={
        'vente':User.objects.filter(type="vente"),

    }
    return render(request, template_name, context)
