from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=40, verbose_name='username')
    password = models.CharField(max_length=255, verbose_name='password')

    def __str__(self):
        return self.username

class Cliente(models.Model):
    dni = models.CharField(max_length=9, verbose_name='dni')
    nombre = models.CharField(max_length=40, verbose_name='nombre')
    apellidos = models.CharField(max_length=60, verbose_name='apellidos')
    direccion = models.CharField(max_length=150, verbose_name='direccion')
    fechaNacimiento = models.DateField(verbose_name='fechaNacimiento')
    fechaAlta = models.DateField(verbose_name='fechaAlta')
    activo = models.BooleanField(verbose_name='activo')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="idUsuario")

    def __str__(self):
        return self.nombre + " " + self.apellidos + " " + self.usuarios.username

class Empleado(models.Model):
    dni = models.CharField(max_length=9, verbose_name='dni')
    nombre = models.CharField(max_length=40, verbose_name='nombre')
    apellidos = models.CharField(max_length=60, verbose_name='apellidos')
    direccion = models.CharField(max_length=150, verbose_name='direccion')
    biografia = models.CharField(max_length=255, verbose_name='biografia')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="idUsuario")

    def __str__(self):
        return self.nombre + "  " + self.apellidos + " " + self.usuarios.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='nombre')
    foto = models.ImageField(upload_to="photos/", verbose_name="foto")

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    titulo = models.CharField(max_length=150, verbose_name='titulo')
    descripcion = models.CharField(max_length=255, verbose_name='descripcion')
    nivel = models.IntegerField(verbose_name='nivel')
    fechaInicio = models.DateField(verbose_name='fechaInicio')
    fechaFin = models.DateField(verbose_name='fechaFin')
    informeFinal = models.CharField(max_length=255, verbose_name='informeFinal')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name='idEmpleado', related_name='empleado')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='idCategoria', related_name='categoria')

    def __str__(self):
        return self.titulo

class Participa(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='idCliente', related_name='cliente')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='idProyecto', related_name='proyecto')
    fechaInscripcion = models.DateField(verbose_name='fechaInscripcion')
    rol = models.CharField(max_length=100, verbose_name='rol')

