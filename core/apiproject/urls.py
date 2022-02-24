from core.apiproject.views import *
from django.urls import path

app_name = 'apiproject'

urlpatterns = [
    path('login', VistaInicioSesion.as_view()),
    path('historial', HistorialCliente.as_view()),
]