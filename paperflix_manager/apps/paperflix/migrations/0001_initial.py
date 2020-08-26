# Generated by Django 3.0.5 on 2020-08-26 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id_category', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255, verbose_name='Categoria')),
                ('status', models.BooleanField(default=True, verbose_name='Activo/Inactivo')),
            ],
        ),
        migrations.CreateModel(
            name='Papers',
            fields=[
                ('id_paper', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Titulo')),
                ('description', models.CharField(max_length=255, verbose_name='Descripcion')),
                ('publication_year', models.IntegerField(verbose_name='Fecha de publicacion')),
                ('author', models.CharField(max_length=255, verbose_name='Autor')),
                ('language', models.CharField(max_length=255, verbose_name='Idioma')),
                ('number_pages', models.IntegerField(null=True)),
                ('viewed', models.IntegerField(null=True)),
                ('downloads', models.IntegerField(null=True)),
                ('pos_rate', models.IntegerField(null=True)),
                ('neg_rate', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Papers',
                'verbose_name_plural': 'Paper',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=255, verbose_name='Contraseña')),
                ('status', models.BooleanField(default=True, verbose_name='Activo/Inactivo')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Fecha de creacion')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='PapersUser',
            fields=[
                ('id_papersuser', models.AutoField(primary_key=True, serialize=False)),
                ('rated', models.IntegerField()),
                ('id_paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperflix.Papers')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperflix.Users')),
            ],
            options={
                'verbose_name': 'Paper',
                'verbose_name_plural': 'Papers',
            },
        ),
        migrations.CreateModel(
            name='CategoryPaper',
            fields=[
                ('id_categorypaper', models.AutoField(primary_key=True, serialize=False)),
                ('id_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperflix.Categories')),
                ('id_paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperflix.Papers')),
            ],
        ),
    ]
