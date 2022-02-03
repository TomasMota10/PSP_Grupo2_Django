from django.http.response import HttpResponseRedirect
from core.project.models import Project
from core.user.models import User
from django.contrib import messages

def same_user(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        
        if not request.user.is_superuser:
            print(user.id)
            print(request.user.id)
            if not (user.id == request.user.id):
                messages.success(request, 'Esta acción no esta permitida o no se encuentra disponible.')
                if request.user.role_user == 'Cliente':
                    return HttpResponseRedirect('/')
                elif request.user.role_user == 'Empleado':
                    return HttpResponseRedirect('/')

        return func(request, *args, **kwargs)

    return check_and_call

def is_admin(func):
    def check_and_call(request, *args, **kwargs):

        if not (request.user.is_superuser):
            messages.success(request, 'Esta acción no esta permitida o no se encuentra disponible.')
            return HttpResponseRedirect('/')

        return func(request, *args, **kwargs)

    return check_and_call

def is_client(func):
    def check_and_call(request, *args, **kwargs):

        if not (request.user.role_user == 'Cliente'):
            messages.success(request, 'Esta acción no esta permitida o no se encuentra disponible.')
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)

    return check_and_call

def is_employee(func):
    def check_and_call(request, *args, **kwargs):

        if not (request.user.role_user == 'Empleado'):
            messages.success(request, 'Esta acción no esta permitida o no se encuentra disponible.')
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)

    return check_and_call

def owns_project(func):
    def check_and_call(request, *args, **kwargs):
        pk= kwargs['pk']
        project_owner=Project.objects.get(pk=pk).empleado

        if not request.user.is_superuser:
            if not (project_owner == request.user):
                messages.success(request, 'Esta acción no esta permitida o no se encuentra disponible.')
                if request.user.role_user == 'Cliente':
                    return HttpResponseRedirect('/')
                elif request.user.role_user == 'Empleado':
                    return HttpResponseRedirect('/')
            
        return func(request, *args, **kwargs)
        
    return check_and_call

    