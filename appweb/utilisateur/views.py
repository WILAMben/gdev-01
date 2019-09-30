from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
# Create your views here.
from commande.models import Commande
from panier.models import Panier_user
from produit.models import Produit, ProduitsFavorite
from utilisateur.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random
from datetime import datetime, timedelta

def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = auth.authenticate(username=username, password=password)
       

        if user is not None:

        
            if user.confirmed == False :
                if user.type != "vente":
                        messages.success(request, 'compte non confirmer verifier votre boite email')
                else:
                    messages.success(request, 'non confirmer')
                auth.logout(request)
                return HttpResponseRedirect('/produit/')

            else:
                request.session['comp1'] = 0
                request.session['comp2'] = 0
                request.session['comp3'] = 0
                auth.login(request, user)
                messages.success(request, 'rak mconicti')
                return HttpResponseRedirect('/produit/')



        else:
            if 'nbr' not in request.session:
                request.session['nbr'] =0

            request.session['nbr']=request.session['nbr']+1
            if request.session['nbr'] > 3 :
                request.session['try']='non'
            #request.session.set_expiry(300)
            messages.success(request, 'Email ou Mot de passe invalide')
            return HttpResponseRedirect('/produit/')


    else:

        return HttpResponse("<h1> makach post ga3 </h1>")




def lougout_view(request):
    if request.method== 'POST':
        auth.logout(request)
        return HttpResponseRedirect('/produit/')


def registre_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        adresse = request.POST["adresse"]
        wilaya = request.POST["wilaya"]
        telephone = request.POST["telephone"]
        rc = request.POST["rc"]
        lm = request.POST["lm"]
        jj = request.POST["jj"]
        ll = request.POST["ll"]
        type = request.POST["type_client"]
        print(type)
        print('jjjhkj')


        #generer une kle dactivation
        print("boucle")
        while True:

            key = ''
            g = random.randint(2, 15)
            while len(key) < g:
                n = random.randint(0, 9)
                key += str(n)
                print(key)
            #k = int(key)


            if not User.objects.filter(activation_key=key).exists():
                break

        print("mor boucle")

        if password1 != "///":

                if User.objects.filter(username=username).exists():
                    print("mor hjgghsdgjhgdkjghhdg")
                    messages.error(request, "username taken")
                    template_name = 'utilisateur/registre.html'
                    return render(request, template_name)

                else:

                    if User.objects.filter(email=email).exists():
                        print("mor kkkkkkkkkkkkkkkkkkkkk")
                        messages.error(request, "email taken")
                        template_name = 'utilisateur/registre.html'
                        return render(request, template_name)

                    else:
                        print("kolch mrigli")
                        user= User.objects.create_user(username=username,email=email,password=password1,wilaya_user=wilaya, activation_key=key, type="user",type_sp=type,
                                                       first_name=first_name,last_name=last_name,adresse_user=adresse,telephone_user=telephone,rc= rc,mi=lm, li=jj,nis=ll)
                        #auth.login(request, user)
                        user.active_user_email()
                        auth.logout(request)
                        #messages.error(request, "verifier votre email et confirmer votre compte pour connecter")
                        #return HttpResponseRedirect('/produit/')
                        return HttpResponseRedirect('/utilisateur/registre/key/?key='+ str(user.id))


        else:
            print("mor hhhhhhhhhhhhhhhhh")
            messages.error(request,"password not match")
            template_name = 'utilisateur/registre.html'
            return render(request, template_name)


    else:
        print("mor sssssssssssssssssssss")
        template_name= 'utilisateur/registre.html'
        return render(request ,template_name)






def renvoyer_code(request):
    id = request.GET.get('id')
    while True:

        key = ''
        g = random.randint(2, 15)
        while len(key) < g:
            n = random.randint(0, 9)
            key += str(n)
            print(key)
        # k = int(key)

        if not User.objects.filter(activation_key=key).exists():
            break


    User.objects.filter(id=id).update(activation_key=key)
    user=User.objects.get(id=id)
    user.active_user_email()
    auth.logout(request)
    return HttpResponseRedirect('/utilisateur/registre/key/?key='+ str(user.id))

def keyRegistre_view(request):
    if request.method == 'POST':
        id = request.POST["inp"]
        sr = User.objects.get(activation_key=id)
        User.objects.filter(activation_key=id).update(confirmed=True)
        login(request, sr, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, 'rak mconicti')



        #suprimi li machi confirmer
        day = datetime.now() - timedelta(days=2)
        User.objects.filter(Q(date_joined__lte=day) & Q(confirmed=False) ).delete()





        return HttpResponseRedirect('/produit/')

    key = request.GET.get('key')

    usr=User.objects.get(id=key).activation_key
    context={
        'key':usr,
        'id':key,
    }
    template_name = 'utilisateur/keyRegistre.html'
    auth.logout(request)
    return render(request, template_name, context)



























def activation(request, codeActivation):
    us = User.objects.filter(activation_key=codeActivation)
    context = {
        'user': us
    }

    template_name = 'utilisateur/welcom.html'
    return render(request, template_name, context)



#def activated(request, codeActivation):
 #   if request.method== 'POST':
  #      id = request.POST["inp"]
   #     sr = User.objects.get(activation_key=codeActivation)
    #    name = sr.username
    #   passw = sr.password
     #   User.objects.filter(id=id).update(confirmed=True)
      #  login(request, sr, backend='django.contrib.auth.backends.ModelBackend')
        #user = auth.authenticate(username=name, password=passw)
        #auth.login(request, user)
       # messages.success(request, 'rak mconicti')
        #return HttpResponseRedirect('/produit/')


def mdpOublier(request):
    if request.method== 'POST':
        username = request.POST["login"]

        if not User.objects.filter(username=username).exists():
            messages.error(request, "ma3endekch compte 3ami")
            template_name = 'utilisateur/mdpOublier.html'
            return render(request, template_name)

        else:
            print("qqqqqqqqqqqqqqqqqqqq")
            user = User.objects.get(username=username)
            if user.confirmed== False:
                messages.error(request, "vous devez d'abord activer votre compte")
                template_name = 'utilisateur/mdpOublier.html'
                return render(request, template_name)
            else:
                while True:

                    key = ''
                    g = random.randint(2, 15)
                    while len(key) < g:
                        n = random.randint(0, 9)
                        key += str(n)
                        print(key)
                    # k = int(key)

                    if not User.objects.filter(activation_key=key).exists():
                        break
                User.objects.filter(username=username).update(activation_key=key)
                usere = User.objects.get(username=username, activation_key=key)


                usere.mdpEmail()
                template_name = 'utilisateur/success_send_mail.html'
                return render(request, template_name)



    template_name = 'utilisateur/mdpOublier.html'
    return render(request, template_name)




def initmdp(request, mdpInit):
    us = User.objects.filter(activation_key=mdpInit)
    context = {
        'user': us,
        'mdpInit':mdpInit,
    }

    template_name = 'utilisateur/initMdpForm.html'
    return render(request, template_name, context)



def initmdpFinal(request):
    if request.method== 'POST':
        id_user = request.POST["inp"]
        passwo = request.POST["mdpinit"]
        # User.objects.filter(id=id_user).update(password=passwo)
        u = User.objects.get(id=id_user)
        u.set_password(passwo)
        u.save()
        while True:

            key = ''
            g = random.randint(2, 15)
            while len(key) < g:
                n = random.randint(0, 9)
                key += str(n)
                print(key)
            #k = int(key)


            if not User.objects.filter(activation_key=key).exists():
                break
        User.objects.filter(id=id_user).update(activation_key=key)
        us = User.objects.get(id=id_user)
        auth.authenticate(username=us.username, password=us.password)
        return HttpResponseRedirect('/produit/')


def contactEmail(request):
    if request.method== 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        print(name)
        print(email)
        print(subject)
        print(message)

        print("tttttttttttttttttttttttttt")
        context = {
            "name": name,
            "email": email,
            "message":message,
        }
        messagee = render_to_string("utilisateur/contact.txt", context)

        print("9bel mail")
        send_mail(
            subject,
            messagee,
            'didaben.noreply@gmail.com',
            ['didabenbatna@gmail.com'],
            fail_silently=False,
        )
        print("moraha")
        return HttpResponse('votre email a ete envoyer merci')
    return HttpResponse('mala cv')



def update_info(request):
    if request.method== 'POST':
        id = request.POST["id"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        nom = request.POST["name"]
        Prenom = request.POST["Prenom"]
        tlf = request.POST["tlf"]
        adresse = request.POST["adresse"]
        wilaya = request.POST["wilaya"]
        us = User.objects.get(id=id)
        print(wilaya)
        print(adresse)
        print(tlf)
        print(Prenom)
        print(email)
        print(password1)
    


        if us.type_sp == "revendeur" :
           rc = request.POST["rc"]
           mi = request.POST["mi"]
           li = request.POST["li"]
           nis = request.POST["nis"]

        if  User.objects.filter(username=username).exists() and us.username != username:

                    messages.error(request, "username taken")

                    return HttpResponseRedirect('/utilisateur/update_info/?id=' + str(id))

        else:

                    if User.objects.filter(email=email).exists() and us.email != email:

                        messages.error(request, "email taken")

                        return HttpResponseRedirect('/utilisateur/update_info/?id=' + str(id))

                    else:
                        print("kolch mrigli")
                        
                        us.set_password(password1)
                        us.save()
                        
                        
                        if us.type_sp == "revendeur" :
                            User.objects.filter(id=id).update(rc=rc ,mi=mi, li=li, nis=nis)
                        User.objects.filter(id=us.id).update(username=username,email=email,wilaya_user=wilaya,first_name=nom,last_name=Prenom, adresse_user=adresse,telephone_user=tlf
)
                       #username=username,email=email,wilaya_user=wilaya,first_name=nom,last_name=Prenom, adresse_user=adresse,telephone_user=tlf





    idu = request.GET.get('id')
    akm= User.objects.get(id=idu)
    user = auth.authenticate(username=akm.username, password=akm.password)
    auth.login(request, user)
    template_name = 'utilisateur/update_info.html'
    context = {

        'all': akm,

    }
    return render(request, template_name, context)



def suppCompte(request):
    if request.method== 'POST':
        id = request.POST["id"]
        us = User.objects.get(id=id)
        if Panier_user.objects.filter(id_panier_user=us).exists():
            lap = Panier_user.objects.filter(id_panier_user=us)
            for item_panier in lap:
                m = Panier_user.objects.get(id=item_panier.id)
                Panier_user.delete(m)

        if ProduitsFavorite.objects.filter(id_user=us).exists():
            lap = ProduitsFavorite.objects.filter(id_user=us)
            for item_panier in lap:
                m = ProduitsFavorite.objects.get(id=item_panier.id)
                ProduitsFavorite.delete(m)

        if Commande.objects.filter(id_user=us).exists():

            key = ''
            g = random.randint(9, 15)
            while len(key) < g:
                n = random.randint(0, 9)
                key += str(n)

            User.objects.filter(id=id).update(username=key)
            key = ''
            g = random.randint(9, 15)
            while len(key) < g:
                n = random.randint(0, 9)
                key += str(n)

            User.objects.filter(id=id).update(password=key)

            key = ''
            g = random.randint(9, 15)
            while len(key) < g:
                n = random.randint(0, 9)
                key += str(n)

            User.objects.filter(id=id).update(email=key)


        else:


            p=us
            User.delete(p)




    auth.logout(request)
    return HttpResponseRedirect('/produit/')