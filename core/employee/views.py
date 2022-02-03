from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from core.client.forms import ClientForm
from core.user.forms import UserForm
from core.user.models import User
from core.employee.forms import EmployeeForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.utils.decorators import method_decorator
from core.decorators import *
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import ValidatePermissionRequiredMixin
from core.employee.serializers import EmployeeSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status

class EmployeeListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'employee/list.html'
    # permission_required = '.view_client'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Empleados en AlmaGest.'
        context['employees'] = User.objects.filter(role_user='Empleado')
        context['create_url'] = reverse_lazy('adm:employee_create')
        return context

@method_decorator(is_admin, name="dispatch")
class EmployeeCreateView(LoginRequiredMixin,CreateView):
    model = User
    form_class = EmployeeForm
    template_name = 'employee/create.html'
    success_url = reverse_lazy('login')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        context['title'] = ' Registrar nuevo Empleado en AlmaGest.'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)

        if form.is_valid():
            employee = form.save(commit=False)
            employee.role_user='Empleado'
            employee.save()
            messages.success(request, 'El empleado ha sido registrado correctamente.')
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(self.request, 'El empleado ha sido registrado correctamente.')
        return reverse('adm:employee_list')

@method_decorator(same_user, name="dispatch")
class EmployeeUpdateView(LoginRequiredMixin,CreateView):
    model = User
    form_class = EmployeeForm
    template_name = 'employee/create.html'
    success_url = reverse_lazy('login')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Edita tu perfil como empleado en AlmaGest.'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

    def get_success_url(self):
        messages.success(self.request, 'Los datos han sido actualizados correctamente.')
        return reverse('adm:employee_list')

class EmployeeDeleteView(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('adm:employee_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Empleado en AlmaGest.'
        context['list_url'] = self.success_url
        return context

    def get_success_url(self):
        messages.success(self.request, 'El empleado ha sido eliminado correctamente.')
        return reverse('adm:employee_list')

#Api REST
# class Employees_APIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         empl = User.objects.filter(role_user = 'Empleado')
#         serializer = EmployeeSerializers(empl, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = EmployeeSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer)


# class Employees_APIView_Detail(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         empl = self.get_object(pk)
#         serializer = EmployeeSerializers(empl)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         empl = self.get_object(pk)
#         serializer = EmployeeSerializers(empl, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_204_NOT_CONTENT)

#     def delete(self,request, pk, format=None):
#         empl = self.get_object(pk)
#         empl.delete()
#         return Response(status=status.HTTP_204_NOT_CONTENT)

# class TestView(APIView):

#     def get(self, request, format=None):
#         return Response({'detail':'GET Response'})

#     def post(self, request, format=None):
#         try:
#             data = request.data
#         except ParseError as error:
#             return Response(
#                 'Invalid JSON - {0}'.format(error.detail),
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if 'user' not in data or 'password' not in data:
#             return Response(
#                 'Wrong credentials',
#                 status = status.HTTP_401_UNAUTHORIZED
#             )

#         user = User.objects.get(username=data['user'])
#         if not user:
#             return Response(
#                 'No default user, please create one',
#                 status = status.HTTP_404_NOT_FOUND
#             )

#         token = Token.objects.get_or_create(user=user)
#         return Response({'detail':'POST answer','token': token[0].key})
