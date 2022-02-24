from django.urls import path
from core.client.views import *
from core.employee.views import *
from core.category.views import *
from core.project.views import *

app_name = 'adm'

urlpatterns = [
    #Clientes
    path('clientes/listado/', ClientListView.as_view(), name='client_list'),
    path('clientes/activar/<int:pk>/', ClientActivateView, name='client_activate'),
    path('clientes/desactivar/<int:pk>/', ClientDeactivateView, name='client_deactivate'),
    path('clientes/crear/', ClientCreateView.as_view(), name='client_create'),
    path('clientes/actualizar/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clientes/eliminar/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    #Empleados
    path('empleados/listado/', EmployeeListView.as_view(), name='employee_list'),
    path('empleados/crear/', EmployeeCreateView.as_view(), name='employee_create'),
    path('empleados/actualizar/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('empleados/eliminar/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),

    #Categorías
    path('categorias/listado/', CategoryListView.as_view(), name='category_list'),
    path('categorias/crear/', CategoryCreateView.as_view(), name='category_create'),
    path('categorias/actualizar/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categorias/eliminar/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    #Proyectos
    path('proyectos/listado/', ProjectListView.as_view(), name='project_list'),
    path('proyectos/crear/', ProjectCreateView.as_view(), name='project_create'),
]
