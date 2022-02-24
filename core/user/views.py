from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.user.forms import UserForm
#from core.user.models import User

#class UserCreateView(CreateView):
#    model = User
#    form_class = UserForm
#    template_name = 'create.html'
#    success_url = reverse_lazy('login')
#    url_redirect = success_url

#    def dispatch(self, request, *args, **kwargs):
#        return super().dispatch(request, *args, **kwargs)

#    def post(self, request, *args, **kwargs):
#        self.object = self.get_object
#        form = self.form_class(request.POST)
#        if form.is_valid():
#            form.save()
#            messages.success(request, 'El usuario ha sido registrado correctamente.')
#            return HttpResponseRedirect(self.get_success_url())
    #    else:
    #        return self.render_to_response(self.get_context_data(form=form))

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['title'] = 'Nuevo Cliente'
    #    context['entity'] = 'Usuarios'
    #    context['list_url'] = self.success_url
    #    context['action'] = 'add'
    #    return context

#class UserUpdateView(LoginRequiredMixin, UpdateView):
#    model = User
#    form_class = UserForm
#    template_name = 'create.html'
#    success_url = reverse_lazy('login')
#    url_redirect = success_url

#    def dispatch(self, request, *args, **kwargs):
#        return super().dispatch(request, *args, **kwargs)

#    def post(self, request, *args, **kwargs):
#        self.object = self.get_object()
#        form = self.get_form()
        
#        if form.is_valid():
#            form.save()
#            messages.success(request, 'El usuario ha sido editado con éxito')
#            return HttpResponseRedirect(self.get_success_url())
#        else:
#            return self.render_to_response(self.get_context_data(form=form))

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['title'] = 'Editar mi perfil'
#        context['entity'] = 'Usuarios'
#        context['list_url'] = self.success_url
#        context['action'] = 'edit'
#        return context