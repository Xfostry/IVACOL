from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperUserCommand

class Command(BaseCreateSuperUserCommand):
    def handle(self, *args, **options):
        # Si se está creando un superuser, asignar rol='admin' automáticamente
        options['rol'] = 'admin'
        super().handle(*args, **options)

    def get_user_data(self, *args, **options):
        data = super().get_user_data(*args, **options)
        data['rol'] = 'admin'
        return data
