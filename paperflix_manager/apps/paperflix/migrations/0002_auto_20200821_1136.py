# Generated by Django 3.0.5 on 2020-08-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paperflix', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=255, verbose_name='Contraseña'),
        ),
    ]
