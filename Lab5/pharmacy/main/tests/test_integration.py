from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import Medicine, Category, Cart, CartItem, Sale, SaleItem
from decimal import Decimal

class ShoppingFlowIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create customer group and add user to it
        self.customer_group = Group.objects.create(name='Customers')
        self.user.groups.add(self.customer_group)
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        # Create test medicines
        self.medicine1 = Medicine.objects.create(
            code='TEST001',
            name='Test Medicine 1',
            description='Test Description 1',
            instructions='Test Instructions 1',
            price=Decimal('10.00'),
            stock=100,
            category=self.category
        )
        
        self.medicine2 = Medicine.objects.create(
            code='TEST002',
            name='Test Medicine 2',
            description='Test Description 2',
            instructions='Test Instructions 2',
            price=Decimal('20.00'),
            stock=50,
            category=self.category
        )

    def test_complete_shopping_flow(self):
        # Step 1: Login
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)
        
        # Step 2: Browse medicine list
        response = self.client.get(reverse('main:medicine_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Medicine 1')
        self.assertContains(response, 'Test Medicine 2')
        
        # Step 3: View medicine detail
        response = self.client.get(
            reverse('main:medicine_detail', kwargs={'pk': self.medicine1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Medicine 1')
        
        # Step 4: Add items to cart
        response = self.client.post(
            reverse('main:add_to_cart', kwargs={'medicine_id': self.medicine1.pk}),
            {'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)
        
        response = self.client.post(
            reverse('main:add_to_cart', kwargs={'medicine_id': self.medicine2.pk}),
            {'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)
        
        # Step 5: View cart
        response = self.client.get(reverse('main:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Medicine 1')
        self.assertContains(response, 'Test Medicine 2')
        
        # Verify cart contents
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 2)
        self.assertEqual(
            cart.items.get(medicine=self.medicine1).quantity,
            2
        )
        self.assertEqual(
            cart.items.get(medicine=self.medicine2).quantity,
            1
        )
        
        # Step 6: Proceed to checkout
        response = self.client.post(reverse('main:checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to success page
        
        # Verify order creation
        sale = Sale.objects.filter(customer=self.user).latest('date')
        self.assertIsNotNone(sale)
        self.assertEqual(sale.items.count(), 2)
        self.assertEqual(
            sale.total_amount,
            Decimal('40.00')  # (2 * 10.00) + (1 * 20.00)
        )
        
        # Verify stock updates
        self.medicine1.refresh_from_db()
        self.medicine2.refresh_from_db()
        self.assertEqual(self.medicine1.stock, 98)  # 100 - 2
        self.assertEqual(self.medicine2.stock, 49)  # 50 - 1
        
        # Step 7: View order history
        response = self.client.get(reverse('main:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Medicine 1')
        self.assertContains(response, 'Test Medicine 2')

class AuthenticationIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_group = Group.objects.create(name='Customers')

    def test_registration_login_flow(self):
        # Step 1: Register new user
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('main:register'), register_data)
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        
        # Verify user creation
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)
        self.assertTrue(user.groups.filter(name='Customers').exists())
        
        # Step 2: Login with new user
        response = self.client.post(reverse('main:login'), {
            'username': 'newuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
        # Step 3: Access protected page
        response = self.client.get(reverse('main:profile'))
        self.assertEqual(response.status_code, 200)
        
        # Step 4: Logout
        response = self.client.get(reverse('main:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        
        # Verify cannot access protected page after logout
        response = self.client.get(reverse('main:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login 