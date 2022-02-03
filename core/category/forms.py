from django.forms import *
from core.category.models import Category

class CategoryForm(ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Category
        fields = ('nombre','foto')
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la categoria',
                }
            ),
            'foto': FileInput(
                attrs={
                }
            )
        }
        