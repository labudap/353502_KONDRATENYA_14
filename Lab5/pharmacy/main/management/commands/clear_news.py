from django.core.management.base import BaseCommand
from main.models import News

class Command(BaseCommand):
    help = 'Delete all existing news articles'

    def handle(self, *args, **kwargs):
        # Delete all news articles
        count = News.objects.all().delete()[0]
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} news articles')
        ) 