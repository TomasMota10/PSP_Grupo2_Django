from django.urls import path
from core.client.views import *

app_name = 'client'

urlpatterns = [
    path('add/', ClientCreateView.as_view(), name='client_create'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
]