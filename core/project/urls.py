from core.project.views import *
from django.urls import path

app_name = 'project'

urlpatterns = [
    path('listado/', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('inscripcion/', ProjectInscriptionView.as_view(), name="project_inscription"),
    path('inscription/create/<int:pk>', InscriptionCreate, name="project_inscription_create"),
    path('clientes/<int:pk>', ProjectClientsView.as_view(), name='project_clients'),
    path('empleados/historial/', ProjectHistoryEmployeesView.as_view(), name='project_employee_history'),
    path('clientes/historial/', ProjectHistoryClientsView.as_view(), name='project_client_history'),
    path('clientes/historial/PDF', ProyectoClientePDF.as_view(), name='project_client_pdf'),
    path('clientes/proximos-proyectos/', UpcomingProject.as_view(), name='project_upcoming'),
    path('proyectos/finalizar/<int:pk>', ProyectoFinalizar, name='project_finish'),
    path('clientes/participacion', ProyectoClientesParticipacion.as_view(), name='project_clients_participation'),
    
]
