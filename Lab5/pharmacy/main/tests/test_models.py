from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from main.models import (
    Department, Category, Supplier, Medicine,
    Review, Promo, Sale, SaleItem
)
from decimal import Decimal

class DepartmentTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Description",
            location="Test Location"
        )

    def test_department_creation(self):
        self.assertEqual(self.department.name, "Test Department")
        self.assertEqual(self.department.description, "Test Description")
        self.assertEqual(self.department.location, "Test Location")

    def test_department_str(self):
        self.assertEqual(str(self.department), "Test Department")

class CategoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "Test Description")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Test Category")

class SupplierTests(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Test Supplier",
            contact_person="John Doe",
            phone="+375 (29) 123-45-67",
            email="test@example.com",
            address="Test Address"
        )

    def test_supplier_creation(self):
        self.assertEqual(self.supplier.name, "Test Supplier")
        self.assertEqual(self.supplier.contact_person, "John Doe")
        self.assertEqual(self.supplier.phone, "+375 (29) 123-45-67")
        self.assertEqual(self.supplier.email, "test@example.com")
        self.assertEqual(self.supplier.address, "Test Address")

    def test_supplier_str(self):
        self.assertEqual(str(self.supplier), "Test Supplier")

    def test_invalid_phone_format(self):
        with self.assertRaises(ValidationError):
            supplier = Supplier(
                name="Invalid Supplier",
                contact_person="John Doe",
                phone="123456789",  # Invalid format
                email="test@example.com",
                address="Test Address"
            )
            supplier.full_clean()

class MedicineTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.supplier = Supplier.objects.create(
            name="Test Supplier",
            contact_person="John Doe",
            phone="+375 (29) 123-45-67",
            email="test@example.com",
            address="Test Address"
        )
        self.medicine = Medicine.objects.create(
            code="TEST001",
            name="Test Medicine",
            description="Test Description",
            instructions="Test Instructions",
            price=Decimal("10.00"),
            stock=100,
            category=self.category
        )
        self.medicine.suppliers.add(self.supplier)

    def test_medicine_creation(self):
        self.assertEqual(self.medicine.code, "TEST001")
        self.assertEqual(self.medicine.name, "Test Medicine")
        self.assertEqual(self.medicine.price, Decimal("10.00"))
        self.assertEqual(self.medicine.stock, 100)
        self.assertEqual(self.medicine.category, self.category)
        self.assertIn(self.supplier, self.medicine.suppliers.all())

    def test_medicine_str(self):
        self.assertEqual(str(self.medicine), "Test Medicine (TEST001)")

    def test_negative_price(self):
        with self.assertRaises(ValidationError):
            medicine = Medicine(
                code="TEST002",
                name="Test Medicine 2",
                description="Test Description",
                instructions="Test Instructions",
                price=Decimal("-10.00"),
                stock=100,
                category=self.category
            )
            medicine.full_clean()

class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.review = Review.objects.create(
            user=self.user,
            rating=5,
            text="Great service!"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.text, "Great service!")

    def test_review_str(self):
        self.assertEqual(str(self.review), f"Review by {self.user.username} - 5 stars")

    def test_invalid_rating(self):
        with self.assertRaises(ValidationError):
            review = Review(
                user=self.user,
                rating=6,  # Invalid rating
                text="Test review"
            )
            review.full_clean()

class PromoTests(TestCase):
    def setUp(self):
        self.promo = Promo.objects.create(
            code="TEST20",
            description="Test promo",
            discount_percent=20,
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=30),
            is_active=True
        )

    def test_promo_creation(self):
        self.assertEqual(self.promo.code, "TEST20")
        self.assertEqual(self.promo.discount_percent, 20)
        self.assertTrue(self.promo.is_active)

    def test_promo_str(self):
        self.assertEqual(str(self.promo), "TEST20 (20% off)")

class SaleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Test Category")
        self.medicine = Medicine.objects.create(
            code="TEST001",
            name="Test Medicine",
            price=Decimal("10.00"),
            category=self.category
        )
        self.sale = Sale.objects.create(
            customer=self.user,
            total_amount=Decimal("20.00")
        )
        self.sale_item = SaleItem.objects.create(
            sale=self.sale,
            medicine=self.medicine,
            quantity=2,
            price=Decimal("10.00")
        )

    def test_sale_creation(self):
        self.assertEqual(self.sale.customer, self.user)
        self.assertEqual(self.sale.total_amount, Decimal("20.00"))

    def test_sale_item_creation(self):
        self.assertEqual(self.sale_item.sale, self.sale)
        self.assertEqual(self.sale_item.medicine, self.medicine)
        self.assertEqual(self.sale_item.quantity, 2)
        self.assertEqual(self.sale_item.price, Decimal("10.00"))

    def test_sale_str(self):
        expected_str = f"Sale {self.sale.id} - {self.sale.date.strftime('%d/%m/%Y')}"
        self.assertEqual(str(self.sale), expected_str) 