from django.test import TestCase
from django.urls import reverse
from asistencia.models import Usuario, FacturaSubida, Notification

class UsuarioModelTest(TestCase):
    def test_creacion_usuario(self):
        usuario = Usuario.objects.create_user(
            username='testuser', password='12345', numero_documento='123',
            tipo_documento='CC', genero='masculino', ciudad='bogota', telefono='123456', direccion='calle 1', rol='usuario', email='test@example.com', first_name='Test', last_name='User'
        )
        self.assertEqual(usuario.username, 'testuser')
        self.assertEqual(usuario.numero_documento, '123')
        self.assertEqual(str(usuario), 'testuser (123)')

class FacturaSubidaModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='factuser', password='12345', numero_documento='456',
            tipo_documento='CC', genero='femenino', ciudad='cali', telefono='654321', direccion='calle 2', rol='usuario', email='fact@example.com', first_name='Fact', last_name='User'
        )

    def test_creacion_factura(self):
        factura = FacturaSubida.objects.create(
            usuario=self.usuario, descripcion='Factura test', numero='F001', nit='900123', categoria='Servicios', monto=1000, tipo_monto='neto'
        )
        self.assertEqual(factura.numero, 'F001')
        self.assertEqual(str(factura), f'Factura F001 de {self.usuario}')

class NotificationModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='notifuser', password='12345', numero_documento='789',
            tipo_documento='CC', genero='otro', ciudad='medellin', telefono='789123', direccion='calle 3', rol='usuario', email='notif@example.com', first_name='Notif', last_name='User'
        )

    def test_creacion_notificacion(self):
        notif = Notification.objects.create(
            user=self.usuario, tipo='info', titulo='Test', mensaje='Mensaje de prueba'
        )
        self.assertEqual(notif.titulo, 'Test')
        self.assertFalse(notif.leida)

class LoginUsuarioTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='fdarwin905@gmail.com',
            email='fdarwin905@gmail.com',
            password='1234',
            numero_documento='999999',
            tipo_documento='CC',
            genero='masculino',
            ciudad='bogota',
            telefono='123456789',
            direccion='Calle 123',
            rol='usuario',
            first_name='Darwin',
            last_name='F',
        )

    def test_login_con_email_y_contraseña(self):
        login = self.client.login(username='fdarwin905@gmail.com', password='1234')
        self.assertTrue(login)
        # Si tienes una vista de inicio, puedes probar el acceso:
        # response = self.client.get(reverse('inicio'))
        # self.assertEqual(response.status_code, 200)
