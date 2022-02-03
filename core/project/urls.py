from core.project.views import *
from django.urls import path

app_name = 'project'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('inscription/', ProjectInscriptionView.as_view(), name="project_inscription"),
    path('inscription/create/<int:pk>', InscriptionCreate, name="project_inscription_create"),
    path('clients/<int:pk>', ProjectClientsView.as_view(), name='project_clients'),
    path('employe/history/', ProjectHistoryEmployeesView.as_view(), name='project_employee_history'),
    path('client/history/', ProjectHistoryClientsView.as_view(), name='project_client_history'),
    path('client/upcomingproject/', UpcomingProject.as_view(), name='project_upcoming'),
]
