from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from main.forms import MedicineForm
from main.models import Category
from decimal import Decimal

class MedicineFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.valid_form_data = {
            'name': 'Test Medicine',
            'description': 'Test Description',
            'instructions': 'Test Instructions',
            'price': '10.00',
            'stock': 100,
            'category': self.category.id,
            'code': 'TEST001'
        }

    def test_valid_form(self):
        form = MedicineForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_price(self):
        form_data = self.valid_form_data.copy()
        form_data['price'] = '-10.00'
        form = MedicineForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_invalid_stock(self):
        form_data = self.valid_form_data.copy()
        form_data['stock'] = -1
        form = MedicineForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_missing_required_fields(self):
        form = MedicineForm(data={})
        self.assertFalse(form.is_valid())
        required_fields = ['name', 'description', 'instructions', 'price', 'stock', 'category', 'code']
        for field in required_fields:
            self.assertIn(field, form.errors)

    def test_form_with_image(self):
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty file for testing
            content_type='image/jpeg'
        )
        form_data = self.valid_form_data.copy()
        form = MedicineForm(data=form_data, files={'image': image_file})
        self.assertTrue(form.is_valid()) 