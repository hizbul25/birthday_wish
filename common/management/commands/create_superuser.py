from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if User.objects.filter(username=config('BIRTHDAY_WISHER_SUPERUSER_USERNAME')).exists():
            self.stdout.write(self.style.WARNING(
                "Superuser is already initialized!"))
        else:
            self.stdout.write(self.style.SUCCESS("Initializing superuser..."))
            try:
                superuser = User.objects.create_superuser(
                    username=config('BIRTHDAY_WISHER_SUPERUSER_USERNAME'),
                    email=config('BIRTHDAY_WISHER_SUPERUSER_EMAIL'),
                    password=config('BIRTHDAY_WISHER_SUPERUSER_PASSWORD'))
                superuser.save()
                self.stdout.write(self.style.SUCCESS("Superuser initialized!"))
            except Exception as e:
                print(e)
