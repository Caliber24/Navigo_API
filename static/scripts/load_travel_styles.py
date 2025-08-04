# load_travel_styles.py
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management.base import BaseCommand
from travel.models import TravelStyle

class Command(BaseCommand):
    help = 'Load travel styles from JSON file'

    def handle(self, *args, **options):
        with open('../json/travel_styles.json', 'r', encoding='utf-8') as f:
            styles = json.load(f)
        
        created_count = 0
        for style in styles:
            obj, created = TravelStyle.objects.get_or_create(
                name=style['name'],
                defaults={
                    'description': style['description'],
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_count} travel styles'))