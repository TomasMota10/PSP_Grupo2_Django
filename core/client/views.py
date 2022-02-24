from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from core.client.forms import ClientForm
from core.user.forms import UserForm
from core.user.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from core.decorators import *
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import ValidatePermissionRequiredMixin

@method_decorator(is_admin, name="dispatch")
class ClientListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'client/list.html'
    # permission_required = '.view_client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['clients'] = User.objects.filter(role_user='Cliente')
        context['create_url'] = reverse_lazy('adm:client_create')
        context['entity'] = 'Clientes'
        return context

def ClientActivateView(request,pk):
    User.objects.filter(pk=pk).update(activo=1)
    messages.success(request, 'El cliente ha sido activado correctamente.')
    url = reverse('adm:client_list')
    return HttpResponseRedirect(url)

def ClientDeactivateView(request,pk):
    User.objects.filter(pk=pk).update(activo=0)
    messages.success(request, 'El cliente ha sido desactivado correctamente.')
    url = reverse('adm:client_list')
    return HttpResponseRedirect(url)

class ClientCreateView(CreateView):
    model = User
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('login')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)    
        context['title'] = '#ADMIN | Registrarse'
        context['list_url'] = self.success_url
        context['action'] = 'Registrar'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.role_user = 'Cliente'
            client.save()
            messages.success(request, 'El cliente ha sido registrado correctamente.')
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    
    def get_success_url(self):
        messages.success(self.request, 'El cliente ha sido registrado correctamente.')
        return reverse('login')


@method_decorator(same_user, name="dispatch")
class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('login')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Edita perfil'
        context['list_url'] = self.success_url
        context['action'] = 'Editar'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Los datos han sido actualizados correctamente.')
        return reverse('adm:client_list')

@method_decorator(same_user, name="dispatch")
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'client/delete.html'
    success_url = reverse_lazy('adm:client_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cliente.'
        context['list_url'] = self.success_url
        return context

    def get_success_url(self):
        messages.success(self.request, 'El cliente ha sido eliminado correctamente.')
        return reverse('adm:client_list')


