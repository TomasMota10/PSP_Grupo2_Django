from django.db import models
from core.user.models import User
from core.category.models import Category

class Project(models.Model):
    titulo = models.CharField(max_length=150, verbose_name='Título del Proyecto')
    descripcion = models.CharField(max_length=255, verbose_name='Descripción del Proyecto')
    nivel = models.IntegerField(verbose_name='Nivel')
    fechaInicio = models.DateField(verbose_name='Fecha de Inicio del proyecto')
    fechaFin = models.DateField(verbose_name='Fecha de Fin del Proyecto')
    informePrevio= models.CharField(max_length=255, verbose_name='Informe Previo del Proyecto')
    informeFinal = models.CharField(max_length=255, verbose_name='Informe Final del Proyecto')
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Empleado destinado', related_name='empleado')
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría asociada', related_name='categoria')

    def __str__(self):
        return self.titulo

class Participa(models.Model):
    class ParticipaType(models.TextChoices):
        NoRol='Sin ningún rol asignado',('Sin ningún rol asignado')
        JefeProyecto='Jefe de Proyecto',('Jefe de Proyecto')
        AnalistaProgramador='Analista Programador',('Analista Programador')
        DesarrolloSeniorBack='Desarrollador Senior en Back-End',('Desarrollador Senior en Back-End')
        DesarrolloJuniorBack='Desarrollador Junior en Back-End',('Desarrollador Senior en Back-End')
        DesarrolloSeniorFront='Desarrollador Senior en Front-End',('Desarrollador Senior en Front-End')
        DesarrolloJuniorFront='Desarrollador Junior en Front-End',('Desarrollador Senior en Front-End')
        DesarrolloSeniorFull='Desarrollador Senior completo en las areas de programación',('Desarrollador Senior completo en las areas de programación')
        DesarrolloJuniorFull='Desarrollador Junior completo en las areas de programación',('Desarrollador Junior completo en las areas de programación')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cliente')
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Proyecto')
    fechaInscripcion = models.DateField(verbose_name='Fecha de inscripción')
    rol = models.CharField(max_length=100,default=ParticipaType.NoRol, verbose_name='Rol', choices=ParticipaType.choices)

    # def __str__(self):
        # return self.cliente + ' ' + self.proyecto + ' ' + self.fechaInscripcion + ' ' + self.rol 
