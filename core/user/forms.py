from django.forms import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm

from core.user.models import User

class UserForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['first_name'].widget.attrs['autofocus'] = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username','email','password')
        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'example@example.com',
                }
            ),
            'password': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese una contraseña',
                }
            ),
        }

        exclude = ['groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user           