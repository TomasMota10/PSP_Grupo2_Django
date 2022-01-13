from django.forms import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm

from core.user.models import User


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name','last_name','direccion','fechaNacimiento','dni','username'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'fechaNacimiento': DateInput(
                format='%d-%m-%Y',
                attrs={
                    'value': datetime.now().strftime('%d-%m-%Y'),
                    'placeholder': '01-01-2022',
                                       }
                    ),
            'dni': TextInput(
                attrs={ 
                    'placeholder': '00000000A'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre de usuario',
                }
            ),
        }
        exclude = ['groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user