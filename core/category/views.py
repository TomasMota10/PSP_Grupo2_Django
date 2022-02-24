from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from core.client.forms import ClientForm
from core.category.forms import CategoryForm
from core.user.models import User
from core.category.models import Category
from core.employee.forms import EmployeeForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import ValidatePermissionRequiredMixin

from core.decorators import *
from django.utils.decorators import method_decorator
# Create your views here.
@method_decorator(is_admin, name="dispatch")
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/list.html'
    # permission_required = '.view_client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorías'
        context['categories'] = Category.objects.all()
        context['create_url'] = reverse_lazy('adm:category_create')
        return context

@method_decorator(is_admin, name="dispatch")
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    # permission_required = '.view_client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar nueva Categoría.'
        context['list_url'] = reverse_lazy('adm:category_list')
        context['action'] = 'Añadir'
        return context

    def get_success_url(self):
        messages.success(self.request, 'La categoría ha sido añadida correctamente.')
        return reverse('adm:category_list')

@method_decorator(is_admin, name="dispatch")
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    # permission_required = '.view_client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Categoría'
        context['list_url'] = reverse_lazy('adm:category_list')
        return context

    def get_success_url(self):
        messages.success(self.request, 'La categoría ha sido actualizada correctamente.')
        return reverse('adm:category_list')

@method_decorator(is_admin, name="dispatch")
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('adm:category_list')
    # permission_required = 'adm..delete_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object.delete()
        messages.success(request, 'La categoría ha sido eliminada correctamente.')
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Categoría'
        context['list_url'] = self.success_url
        return context
        