from rest_framework import serializers
from core.user.models import User

class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nombre','apellidos','dni','direccion','biografia','username','email','password')
        