from django.core.management.base import BaseCommand
from main.models import Medicine, Category, Supplier
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample medicines'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = {
            'Pain Relief': 'Medications for managing various types of pain and fever',
            'Supplements': 'Vitamins and mineral supplements for health maintenance',
            'Prescription': 'Prescription medications that require doctor consultation'
        }

        category_objects = {}
        for name, description in categories.items():
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            category_objects[name] = category
            if created:
                self.stdout.write(f'Created category: {name}')

        # Create default supplier if not exists
        supplier, _ = Supplier.objects.get_or_create(
            name='PharmaCorp',
            defaults={
                'contact_person': 'John Doe',
                'email': 'contact@pharmacorp.com',
                'phone': '+1234567890',
                'address': '123 Pharma Street'
            }
        )

        medicines_data = [
            {
                'code': 'PARA001',
                'name': 'Paracetamol 500mg',
                'description': 'Pain reliever and fever reducer',
                'instructions': 'Take 1-2 tablets every 4-6 hours as needed. Do not exceed 8 tablets in 24 hours.',
                'price': Decimal('5.99'),
                'stock': 100,
                'category': 'Pain Relief'
            },
            {
                'code': 'IBUP001',
                'name': 'Ibuprofen 200mg',
                'description': 'Anti-inflammatory pain reliever',
                'instructions': 'Take 1-2 tablets every 4-6 hours after meals. Do not exceed 6 tablets in 24 hours.',
                'price': Decimal('6.99'),
                'stock': 85,
                'category': 'Pain Relief'
            },
            {
                'code': 'ASPI001',
                'name': 'Aspirin 100mg',
                'description': 'Blood thinner and pain reliever',
                'instructions': 'Take 1 tablet daily with water after meals.',
                'price': Decimal('4.99'),
                'stock': 120,
                'category': 'Pain Relief'
            },
            {
                'code': 'VITA001',
                'name': 'Vitamin D3 2000IU',
                'description': 'Vitamin D supplement',
                'instructions': 'Take 1 tablet daily with food.',
                'price': Decimal('11.99'),
                'stock': 150,
                'category': 'Supplements'
            },
            {
                'code': 'MAGN001',
                'name': 'Magnesium 400mg',
                'description': 'Mineral supplement',
                'instructions': 'Take 1 tablet daily with evening meal.',
                'price': Decimal('10.99'),
                'stock': 100,
                'category': 'Supplements'
            },
            {
                'code': 'CALC001',
                'name': 'Calcium 500mg',
                'description': 'Essential mineral for bone health',
                'instructions': 'Take 1 tablet twice daily with meals.',
                'price': Decimal('9.99'),
                'stock': 120,
                'category': 'Supplements'
            },
            {
                'code': 'AMOX001',
                'name': 'Amoxicillin 500mg',
                'description': 'Antibiotic for bacterial infections',
                'instructions': 'Take 1 capsule every 8 hours with or without food. Complete the full course as prescribed.',
                'price': Decimal('12.99'),
                'stock': 50,
                'category': 'Prescription'
            },
            {
                'code': 'METF001',
                'name': 'Metformin 500mg',
                'description': 'Diabetes medication',
                'instructions': 'Take 1 tablet twice daily with meals.',
                'price': Decimal('9.99'),
                'stock': 60,
                'category': 'Prescription'
            },
            {
                'code': 'OMEP001',
                'name': 'Omeprazole 20mg',
                'description': 'Acid reflux and heartburn relief',
                'instructions': 'Take 1 capsule daily before breakfast. Do not crush or chew.',
                'price': Decimal('8.99'),
                'stock': 75,
                'category': 'Prescription'
            },
            {
                'code': 'CETI001',
                'name': 'Cetirizine 10mg',
                'description': 'Antihistamine for allergy relief',
                'instructions': 'Take 1 tablet daily. May cause drowsiness.',
                'price': Decimal('7.49'),
                'stock': 90,
                'category': 'Prescription'
            }
        ]

        for medicine_data in medicines_data:
            category = category_objects[medicine_data['category']]
            medicine, created = Medicine.objects.get_or_create(
                code=medicine_data['code'],
                defaults={
                    'name': medicine_data['name'],
                    'description': medicine_data['description'],
                    'instructions': medicine_data['instructions'],
                    'price': medicine_data['price'],
                    'stock': medicine_data['stock'],
                    'category': category
                }
            )
            
            if created:
                medicine.suppliers.add(supplier)
                self.stdout.write(f'Created medicine: {medicine.name}') 