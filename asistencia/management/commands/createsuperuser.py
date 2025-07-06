from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperUserCommand
from django.core.management.base import CommandError
from django.utils.text import capfirst

class Command(BaseCreateSuperUserCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--rol', dest='rol', default=None, help='Rol del usuario (admin, usuario, etc)')

    def handle(self, *args, **options):
        rol = options.get('rol')
        # Si no se pasa por argumento, pedirlo por input interactivo
        if rol is None:
            rol = input(capfirst('Rol del usuario (admin, usuario, etc): '))
            if not rol:
                raise CommandError('El campo rol es obligatorio.')
        options['rol'] = rol
        super().handle(*args, **options)

    def get_user_data(self, *args, **options):
        data = super().get_user_data(*args, **options)
        data['rol'] = options['rol']
        return data
