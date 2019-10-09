from django.contrib import admin
from .models import Pub, Blog, ImageVente

# Register your models here.
admin.site.register(Pub)
admin.site.register(Blog)
admin.site.register(ImageVente)