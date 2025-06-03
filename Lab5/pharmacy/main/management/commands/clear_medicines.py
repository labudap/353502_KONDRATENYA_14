from django.core.management.base import BaseCommand
from main.models import Medicine

class Command(BaseCommand):
    help = 'Delete all existing medicines'

    def handle(self, *args, **kwargs):
        # Delete all medicines
        count = Medicine.objects.all().delete()[0]
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} medicines')
        ) 