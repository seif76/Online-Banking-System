from django.core.management.base import BaseCommand
from accounts.models import Customer
import random

class Command(BaseCommand):
    help = 'Seeds the database with fake customers'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting seeder...')

        # 1. Clear old data (optional)
        Customer.objects.all().delete()

        # 2. Define fake data
        names = [
            'Alice Smith', 'Bob Jones', 'Charlie Brown', 'Diana Prince', 
            'Evan Wright', 'Fiona Gallagher', 'George Michael', 'Hannah Montana'
        ]
        
        # 3. Create records
        for name in names:
            email = f"{name.lower().replace(' ', '.')}@example.com"
            balance = round(random.uniform(100.00, 5000.00), 2)
            
            Customer.objects.create(
                name=name,
                email=email,
                balance=balance
            )
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(names)} customers!'))