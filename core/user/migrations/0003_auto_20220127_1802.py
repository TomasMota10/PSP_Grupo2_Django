# Generated by Django 3.1.2 on 2022-01-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220126_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role_user',
            field=models.CharField(choices=[('Cliente', 'Cliente'), ('Empleado', 'Empleado'), ('Administrador', 'Administrador')], max_length=50, verbose_name='role'),
        ),
    ]

    