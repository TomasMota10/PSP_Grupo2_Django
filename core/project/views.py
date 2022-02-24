from ast import Try
from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy,reverse
from core.client.forms import ClientForm
from core.project.forms import ProjectForm
from core.user.models import User
from core.category.models import Category
from core.project.models import Project, Participa
from core.employee.forms import EmployeeForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import ValidatePermissionRequiredMixin

from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from core.decorators import *
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(is_employee, name="dispatch")
class ProjectListView(LoginRequiredMixin, ListView):
    paginate_by = 6
    page_kwarg = 'page'
    status_kwarg = 'status'
    model = Project
    ordering = ['fechaFin']
    template_name = 'project/list.html'
    # permission_required = '.view_client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Proyectos.'
        context['projects'] = Project.objects.filter(empleado=self.request.user, fechaFin__gte=datetime.today()+timedelta(days=+1)).order_by('fechaFin')
        context['create_url'] = reverse_lazy('project:project_create')
        return context

@method_decorator(is_employee, name="dispatch")
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create.html'
    # permission_required = '.view_client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar un nuevo Proyecto.'
        context['list_url'] = reverse_lazy('project:project_list')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.empleado = User.objects.filter(pk=self.request.user.id).first()
            project.save()
            messages.success(request, 'El proyecto ha sido registrado correctamente.')
            return HttpResponseRedirect(reverse('project:project_list'))
        else:
            return self.render_to_response(self.get_context_data(form=form))

@method_decorator(owns_project, name="dispatch")
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Proyect.'
        context['list_url'] = reverse_lazy('project:project_list')
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'El proyecto ha sido actualizado correctamente.')
        return reverse('project:project_list')
@method_decorator(owns_project, name="dispatch")
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('project:project_list')
    # permission_required = 'adm..delete_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'El proyecto ha sido eliminado correctamente.')
        return reverse('project:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Proyecto.'
        context['list_url'] = self.success_url
        return context

@method_decorator(is_employee, name="dispatch")
class ProjectHistoryEmployeesView(LoginRequiredMixin, ListView):
    template_name = 'project/listP.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial de Proyectos'
        context['projects'] = Project.objects.filter(empleado=self.request.user, fechaFin__lt = datetime.today()+timedelta(days=+1)).order_by('-fechaFin')
        return context

    def post(self, request, *args, **kwargs):
         Project.objects.filter(pk=self.request.POST.get('id')).update(informeFinal=self.request.POST.get('informeFinal'))
         messages.success(request, 'Informe final actualizado con éxito')
         url = reverse('project:project_employee_history')
         return HttpResponseRedirect(url)

    # def get_queryset(self):
        # return Project.objects.filter(empleado=self.request.user, fechaFin__lt = datetime.now() )
@method_decorator(is_client, name="dispatch")
class ProjectHistoryClientsView(LoginRequiredMixin, ListView):
    template_name = 'project/listP.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial de Proyectos.'
        projects = Project.objects.filter(participa__cliente = self.request.user, fechaFin__lt = datetime.now()).order_by('fechaFin')
        print(projects)
        context['projects'] = projects
        return context

    def post(self, request, *args, **kwargs):
        fechaIni = self.request.POST.get('fechaIni',None)
        fechaFin = self.request.POST.get('fechaFin',None)
        projects = Project.objects.filter(participa__cliente = self.request.user, fechaIni__gt = fechaIni, fechaFin__lt = fechaFin).order_by('fechaFin')

@method_decorator(is_client, name="dispatch")
class UpcomingProject(LoginRequiredMixin, ListView):
    template_name = 'project/listP.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Aquí puedes ver los proyectos de la siguiente semana.'
        date = datetime.today()
        week = date.strftime("%V")
        week = int(week) + 1
        projects = Project.objects.filter(fechaInicio__week = week).order_by('-fechaInicio')
        context['projects'] = projects
        return context

@method_decorator(is_client, name="dispatch")
class ProjectInscriptionView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/listC.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idProj = []
        inscripciones = Participa.objects.filter(cliente_id=self.request.user.id)
        for insc in inscripciones:
            idProj.append(insc.proyecto.pk)

        categoria = self.request.GET.get('category', None)
        fechaIni = self.request.GET.get('fechaIni',None)
        fechaFin = self.request.GET.get('fechaFin',None)

        if categoria is not None and fechaIni != '' and fechaFin != '':
            projects = Project.objects.filter(categoria_id=categoria,fechaFin__lt=fechaFin).exclude(pk__in = idProj)
        elif fechaIni is None and fechaFin is None:
            projects = Project.objects.filter().exclude(pk__in = idProj)
        elif fechaIni != '' and fechaFin != '':
            projects = Project.objects.filter(fechaFin__lt=fechaFin).exclude(pk__in = idProj)
        elif categoria is not None and categoria != '0':
            projects = Project.objects.filter(categoria_id=categoria).exclude(pk__in = idProj)
        else:
            projects = Project.objects.filter().exclude(pk__in = idProj)
            # print(projects)

        context['projects'] = projects
        context['categories'] = Category.objects.all()
        context['title'] = 'Lista de Proyectos disponibles.'
        context['create_url'] = reverse_lazy('project:project_inscription')
        return context    

@method_decorator(owns_project, name="dispatch")
class ProjectClientsView(LoginRequiredMixin, ListView):
    paginate_by = 6
    page_kwarg = 'page'
    status_kwarg = 'status'
    model = Participa
    ordering = ['pk']
    template_name = 'project/listPC.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes inscritos en este proyecto.'       
        context['page_obj'] = Participa.objects.filter(proyecto_id=self.kwargs.get('pk'))       
        # print(context['page_obj'])
        context['roles']=Participa.ParticipaType
        return context

    def post(self, request, *args, **kwargs):
        Participa.objects.filter(proyecto_id=self.kwargs.get('pk'),cliente_id=self.request.POST.get('cliente_id')).update(rol=self.request.POST.get('rol'))
        messages.success(request, 'Se le ha asignado el rol al usuario correctamente.')
        return HttpResponseRedirect(reverse('project:project_clients', kwargs={'pk': self.kwargs.get('pk')}))

@method_decorator(is_employee, name="dispatch")
class ProyectoClientesParticipacion(LoginRequiredMixin, ListView):
     model = Project
     template_name = 'project/list2.html'

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['projects'] = Project.objects.filter(empleado=self.request.user)
         context['roles'] = Participa.ParticipaType
         context['title'] = 'Clientes que se encuentra en nuestros proyectos'

         rol = self.request.GET.get('rol', None)
         project = self.request.GET.get('project',None)

         if rol is not None and project is None:
             participations = Participa.objects.filter(proyecto__empleado = self.request.user, rol = rol)
         elif rol is not None and project is not None:
             participations = Participa.objects.filter(proyecto__empleado = self.request.user, rol = rol, proyecto = project)
         else:
             participations = Participa.objects.filter(proyecto__empleado = self.request.user)

         context['participations'] = participations
         return context

class ProyectoClientePDF(TemplateView):
    model = Project 
    template_name = 'project/proyectoCliente.html' 

    def get_context_data(self, **kwargs):
        context = super(ProyectoClientePDF, self).get_context_data(**kwargs)
        fechaIni = self.request.GET.get('fechaIni',None)
        fechaFin = self.request.GET.get('fechaFin',None)
        projects = Project.objects.filter(participa__cliente = self.request.user, fechaInicio__gte = fechaIni, fechaFin__lt = fechaFin).order_by('-fechaFin')
        context['projects'] = projects
        print(self.request.GET.get('fechaIni'))
        return context 

    def render_to_response(self, context, **kwargs):
        template_path = 'project/proyectoCliente.html'
        context = {'projects': context['projects']}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Informes.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
        html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

@is_client       
def InscriptionCreate(request,pk):
    project = Project.objects.filter(pk=pk).first()
    if project is not None:
        inscripcion = Participa()
        inscripcion.cliente = request.user
        inscripcion.proyecto = project
        inscripcion.fechaInscripcion = datetime.today()
        inscripcion.save()

        messages.success(request, 'Se ha apuntado en el proyecto correctamente.')
    else:
        messages.success(request, 'Oh oh, usted no se ha podido inscribir correctamente en este proyecto.')
    
    url = reverse('project:project_inscription')
    return HttpResponseRedirect(url)

@owns_project
def ProyectoFinalizar(request,pk):
     project = Project.objects.filter(pk=pk).first()

     if project is not None:
         Project.objects.filter(pk=pk).update(fechaFin=datetime.today())
         messages.success(request, 'El proyecto ha sido finalizado correctamente.')
         url = reverse('project:project_employee_history')

     return HttpResponseRedirect(url)
    
    # permission_required = '.view_client'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Lista de Proyectos.'
    #     context['projects'] = Project.objects.all()
    #     context['create_url'] = reverse_lazy('project:project_inscription')
    #     return context
    
    