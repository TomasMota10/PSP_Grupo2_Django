from django.forms import *
from core.project.models import Project, Participa

class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['titulo','descripcion','nivel','fechaInicio','fechaFin','categoria']
        widgets = {
            'titulo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el título del proyecto.',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripción del proyecto.',
                }
            ),
            'Nivel': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nivel de dificultad del proyecto.',
                }
            ),
            'fechaInicio': DateInput(
                attrs={
                   'type': 'date'
                },
                format=('%Y-%m-%d')
            ),
            'fechaFin': DateInput(
                attrs={
                   'type': 'date'
                },
                format=('%Y-%m-%d')
            )
                   
        }

# class InscriptionForm(ModelForm):
#     class Meta:
#         model = Participa
#         fields = "__all__"
