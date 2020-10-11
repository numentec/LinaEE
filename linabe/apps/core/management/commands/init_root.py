from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User

User = get_user_model()

class Command(BaseCommand):
    # Comando para crear super usuario
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = 'root'
            email = 'soporte@numentec.net'
            password = 'KjFrt2020'
            print('Creando superusuario: %s (%s)' % (username, email))
            root = User.objects.create_superuser(email=email, username=username, password=password)
            root.is_active = True
            root.is_admin = True
            root.save()
        else:
            print('Falló la inicialización de root ya que hay usuarios creados con anterioridad')