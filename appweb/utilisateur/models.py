from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random


class User(AbstractUser):
    pass
    #first_name last_name email password
    admin = 'admin'
    user = 'user'
    vente = 'vente'
    directeur = 'directeur'
    enseignant = 'enseignant'
    etudiant = 'etudiant'
    intendant = 'intendant'
    laborantin = 'laborantin'
    revendeur = 'revendeur'

    type_user_sp= [
        (directeur, 'directeur'),
        (enseignant, 'enseignant'),
        (etudiant, 'etudiant'),
        (laborantin, 'laborantin'),
        (intendant, 'intendant'),
        (revendeur, 'revendeur'),

    ]
    type_user = [
        (admin, 'admin'),
        (user, 'user'),
        (vente, 'vente'),
    ]
    type_sp = models.CharField(
        max_length=10,
        choices=type_user_sp,
        null=True,
        blank=True,

    )
    type = models.CharField(
        max_length=5,
        choices=type_user,
    )

    adresse_user = models.CharField(max_length=250, null=True)
    telephone_user = models.CharField(max_length=250, null=True)
    fax_user = models.CharField(max_length=250, null=True,blank=True)
    telephone_portable_user = models.CharField(max_length=250, null=True,blank=True)
    wilaya_user = models.CharField(max_length=50,null=True)
    activation_key = models.CharField(max_length=200,null=True, unique=True,blank=True)
    confirmed = models.BooleanField(default=False)
    rc = models.CharField(max_length=500,null=True,blank=True)
    mi = models.CharField(max_length=50,null=True,blank=True)
    li = models.CharField(max_length=50,null=True,blank=True)
    nis = models.CharField(max_length=50,null=True,blank=True)



    def __str__(self):
        return "ysemouh: "+ str(self.username) +". type ta3o: "+ str(self.type)+"id: "+str(self.id)

    def active_user_email(self):


        activation_url="%s"%(self.activation_key)
        context = {

            "activation_url": activation_url,
            "name": self.username
        }
        message = render_to_string("utilisateur/activation_message.html", context)
        subject = "activate your email"
        send_mail(
            subject,
            message,
            'didaben.noreply@gmail.com',
            [self.email],
            html_message=message,
            fail_silently=False,
        )
# ******************************************************************************************
# ******************************************************************************************


    def mdpEmail(self):

        activation_url="http://www.didaben.com/utilisateur/mdpInit/%s"%(self.activation_key)
        context = {
            "activation_url": activation_url,
            "name": self.username
        }
        message = render_to_string("utilisateur/mdpp.html", context)
        subject = "activate your email"

        send_mail(
            subject,
            message,
            'didaben.noreply@gmail.com',
            [self.email],
            html_message=message,
            fail_silently=False,
        )
     


