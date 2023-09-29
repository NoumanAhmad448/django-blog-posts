from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Run localserver at given port"

    def add_arguments(self, parser):
          pass

    def handle(self, *args, **options):
            server="0.0.0.0:8080"

            self.stdout.write(
                self.style.SUCCESS(f"project is about to run at {server}")
            )
            call_command('runserver',server)
