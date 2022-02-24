from django.db import models
from rest_framework import serializers, viewsets
from core.user.models import User
from core.project.models import Project
from rest_framework.permissions import IsAuthenticated
from core.apiproject.serializers import SerializerCliente


class SerializerProyecto(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['titulo','descripcion','nivel','fechaInicio','fechaFin','categoria_id','empleado_id']


