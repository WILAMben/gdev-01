# Generated by Django 2.2.4 on 2019-09-22 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='Admin/blog/')),
                ('titre', models.CharField(max_length=200, null=True, unique=True)),
                ('description', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('slide', 'slide'), ('demi_slide', 'demi_slide')], max_length=10, null=True)),
                ('img', models.ImageField(upload_to='Admin/pub/')),
                ('titre1', models.CharField(max_length=250, null=True)),
                ('titre2', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]
