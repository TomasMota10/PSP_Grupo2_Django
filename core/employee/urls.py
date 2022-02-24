from django.urls import path
from core.employee.views import *

app_name = 'employee'

urlpatterns = [
    path('add/', EmployeeCreateView.as_view(), name='client_create'),
    path('update/<int:pk>/', EmployeeUpdateView.as_view(), name='client_update'),
    # path('api/employees', Employees_APIView.as_view()),
    # path('api/employees/<int:pk>', Employees_APIView_Detail.as_view()),
    # path('api/token',TestView.as_view())
]
