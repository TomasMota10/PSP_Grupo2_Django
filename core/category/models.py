from django.db import models

class Category(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='nombre')
    foto = models.ImageField(upload_to="photos/", verbose_name="imagen")

    def __str__(self):
        return self.nombre
