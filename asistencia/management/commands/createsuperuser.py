from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperUserCommand

class Command(BaseCreateSuperUserCommand):
    def handle(self, *args, **options):
        options['rol'] = 'admin'  # Asignar rol admin automáticamente
        super().handle(*args, **options)

    def get_user_data(self, *args, **options):
        data = super().get_user_data(*args, **options)
        # Solicitar los campos personalizados si no están en options
        for field in [
            'tipo_documento', 'numero_documento', 'genero', 'ciudad', 'telefono', 'direccion'
        ]:
            if not data.get(field):
                data[field] = input(f'{field.replace("_", " ").capitalize()}: ')
        data['rol'] = 'admin'
        return data
