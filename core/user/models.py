from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# class Usuario(models.Model):
#     username = models.CharField(max_length=40, verbose_name='username')
#     password = models.CharField(max_length=255, verbose_name='password')

#     def __str__(self):
#         return self.username

class User(AbstractUser):
    # is_admin = models.BooleanField(verbose_name='is_admin', default=False)
    is_client = models.BooleanField(verbose_name='is_client', default=False)
    dni = models.CharField(max_length=9, verbose_name='dni',unique = True, default='No', blank = False, null = False)
    # nombre = models.CharField(max_length=40, verbose_name='nombre', null = False)
    # apellidos = models.CharField(max_length=60, verbose_name='apellidos', null = False)
    direccion = models.CharField(max_length=150, verbose_name='direccion', null = False)
    fechaNacimiento = models.DateField(null=True, verbose_name='fechaNacimiento')
    biografia = models.CharField(max_length=255, null=True, verbose_name='biografia')
    # username = models.CharField(max_length=40, unique=True, verbose_name='username')
    # password = models.CharField(max_length=255, verbose_name='password')
    # fechaAlta = models.DateField(verbose_name='fechaAlta', null=True, default=datetime.now)
    # activo = models.BooleanField(verbose_name='activo',default=False, null=True)
    # usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="idUsuario")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.nombre + " " + self.apellidos + " " + self.username
    

    


