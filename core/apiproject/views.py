from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status
from core.user.models import User
from core.project.models import Project
from core.apiproject.serializers import SerializerCliente, SerializerProyecto
from datetime import datetime

class VistaInicioSesion(APIView):
    
    def post(self, request, format=None):

        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user:
            return Response(
                'Wrong credentials',
                status = status.HTTP_401_UNAUTHORIZED
            )

        token = Token.objects.get_or_create(user=user)

        return Response(
            {'user':SerializerCliente(user).data,'token': token[0].key}
            ,
            status=status.HTTP_200_OK)

class HistorialCliente(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, form=None, *args, **kwargs):
        proj = Project.objects.filter(participa__cliente = self.request.user, fechaFin__lt = datetime.now()).order_by('fechaFin')
        serializer = SerializerProyecto(proj, many=True)
        return Response({'projects': serializer.data}, status=status.HTTP_200_OK)