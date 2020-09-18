from django.db import models


# MONGODB
class AdminUsers(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField('Nombre', max_length=255)
    email = models.EmailField('email', null=False, blank=False, unique=True)
    password = models.CharField('Contraseña', max_length=255)
    status = models.BooleanField('Activo/Inactivo', default=True)
    created_at = models.DateField('Fecha de creacion', auto_now=False, auto_now_add=True)


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField('Nombre', max_length=255)
    email = models.EmailField('email', null=False, blank=False, unique=True)
    password = models.CharField('Contraseña', max_length=255)
    status = models.BooleanField('Activo/Inactivo', default=True)
    created_at = models.DateField('Fecha de creacion', auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'

    def __str__(self):
        return self.name


class Papers(models.Model):
    id_paper = models.AutoField(primary_key=True)
    title = models.CharField('Titulo', max_length=255, blank=False, null=False)
    description = models.CharField('Descripcion', max_length=255, blank=False, null=False)
    publication_year = models.IntegerField('Fecha de publicacion', blank=False, null=False)
    author = models.CharField('Autor', max_length=255, blank=False, null=False)
    language = models.CharField("Idioma", max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = 'Papers'
        verbose_name_plural = 'Paper'

    def __str__(self):
        return self.author


class PapersUser(models.Model):
    id_papersuser = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_paper = models.ForeignKey(Papers, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'


class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    category = models.CharField('Categoria', unique=True, max_length=255, blank=False, null=False)
    status = models.BooleanField('Activo/Inactivo', default=True)


class CategoryPaper(models.Model):
    id_categorypaper = models.AutoField(primary_key=True)
    id_paper = models.ForeignKey(Papers, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Categories, on_delete=models.CASCADE)
