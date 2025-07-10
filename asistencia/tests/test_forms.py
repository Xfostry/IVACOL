from django.test import TestCase
from asistencia.forms import UsuarioForm
from asistencia.models import Usuario

class UsuarioFormTest(TestCase):
    def test_formulario_valido(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'tipo_documento': 'CC',
            'numero_documento': '123456',
            'genero': 'masculino',
            'ciudad': 'bogota',
            'telefono': '123456789',
            'direccion': 'Calle 123',
            'rol': 'usuario',
            'email': 'testuser@example.com',
            'password': 'testpass123',
        }
        form = UsuarioForm(data)
        self.assertTrue(form.is_valid())

    def test_formulario_invalido_sin_password(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'tipo_documento': 'CC',
            'numero_documento': '123456',
            'genero': 'masculino',
            'ciudad': 'bogota',
            'telefono': '123456789',
            'direccion': 'Calle 123',
            'rol': 'usuario',
            'email': 'testuser@example.com',
            # Falta password
        }
        form = UsuarioForm(data)
        self.assertFalse(form.is_valid())
