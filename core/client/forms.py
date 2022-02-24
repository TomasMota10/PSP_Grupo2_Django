from django.forms import *
from core.user.models import User

class ClientForm(ModelForm):

    class Meta:
        model = User
        fields = ('nombre','apellidos','dni','direccion','fechaNacimiento','email','username','password')
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': '00000000A',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'fechaNacimiento': DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Ingrese su fecha de nacimiento',
                    'type': 'date'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre de usuario',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'example@example.com',
                }
            ),
            'password': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su contraseña',
                }
            ),

        }

    def save(self, commit=True):
        user = super(ClientForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user