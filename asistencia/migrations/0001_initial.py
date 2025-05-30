# Generated by Django 5.2.1 on 2025-05-30 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('id', models.AutoField(help_text='identificador del usuario', primary_key=True, serialize=False)),
                ('nombres', models.CharField(help_text='nombre del usuario', max_length=100)),
                ('apellidos', models.CharField(help_text='apellido del usuario', max_length=100)),
                ('idtipodocumento', models.IntegerField(help_text='identificador del tipo de documento')),
                ('nodocumento', models.CharField(help_text='numero de documento', max_length=20, unique=True)),
                ('idgenero', models.IntegerField(help_text='identificador de genero')),
                ('idciudad', models.IntegerField(help_text='identificador de la ciudad')),
                ('numero', models.CharField(help_text='numero de contacto', max_length=20)),
                ('correo', models.EmailField(help_text='correo del usuario', max_length=100, unique=True)),
                ('contrasena', models.CharField(help_text='contrasena encriptada', max_length=255)),
                ('direccion', models.CharField(help_text='direccion del usuario', max_length=100)),
                ('idrol', models.IntegerField(help_text='identificador del rol')),
                ('fechaIngreso', models.DateField(blank=True, null=True, verbose_name='Fecha Ingreso')),
            ],
        ),
    ]
