from django.db import models
# Create your models here.
class Pub(models.Model):

    slide = 'slide'
    demi_slide = 'demi_slide'

    ty = [
        (slide, 'slide'),
        (demi_slide, 'demi_slide'),

    ]
    type = models.CharField(
        max_length=10,
        choices=ty,
        null=True,
        blank=True,

    )
    img =  models.ImageField(upload_to='Admin/pub/')
    titre1= models.CharField(max_length=250,null=True, blank=False)
    titre2= models.CharField(max_length=250,null=True, blank=False)


class Blog(models.Model):
    img =  models.ImageField(upload_to='Admin/blog/')
    titre = models.CharField(max_length=200,null=True, unique=True)
    description = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True ,auto_now=False,)
    type= models.CharField(max_length=250,null=True, blank=True)



class ImageVente(models.Model):
    img =  models.ImageField(upload_to='Admin/imageVente/')
    type= models.CharField(max_length=250,null=True, blank=True)

