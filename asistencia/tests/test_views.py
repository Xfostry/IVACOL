from django.test import TestCase
from django.urls import reverse
from asistencia.models import Usuario

class VistasProtegidasTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='vistatest', password='12345', numero_documento='999',
            tipo_documento='CC', genero='masculino', ciudad='bogota', telefono='123', direccion='calle', rol='usuario', email='vista@example.com', first_name='Vista', last_name='Test'
        )

    def test_login_requerido_para_descargar_facturas(self):
        response = self.client.get(reverse('descargar_facturas_pdf'))
        self.assertEqual(response.status_code, 302)  # Redirige a login
        self.client.login(username='vistatest', password='12345')
        response = self.client.get(reverse('descargar_facturas_pdf'))
        self.assertEqual(response.status_code, 200)
