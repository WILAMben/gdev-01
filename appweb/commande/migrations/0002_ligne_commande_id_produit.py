# Generated by Django 2.2.4 on 2019-09-22 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produit', '0001_initial'),
        ('commande', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ligne_commande',
            name='id_produit',
            field=models.ForeignKey(on_delete='cascade', to='produit.Produit'),
        ),
    ]
