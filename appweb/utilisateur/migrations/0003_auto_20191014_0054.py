# Generated by Django 2.2.4 on 2019-10-13 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0002_auto_20191009_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mi',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='rc',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
