from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import Medicine, Category, Cart, CartItem, Review
from decimal import Decimal

class ViewsTestCase(TestCase):
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
        
        # Create test medicine
        self.medicine = Medicine.objects.create(
            code='TEST001',
            name='Test Medicine',
            description='Test Description',
            instructions='Test Instructions',
            price=Decimal('10.00'),
            stock=100,
            category=self.category
        )

    def test_home_view(self):
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_medicine_list_view(self):
        response = self.client.get(reverse('main:medicine_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/medicine_list.html')
        self.assertIn('medicines', response.context)
        self.assertIn(self.medicine, response.context['medicines'])

    def test_medicine_detail_view(self):
        response = self.client.get(
            reverse('main:medicine_detail', kwargs={'pk': self.medicine.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/medicine_detail.html')
        self.assertEqual(response.context['medicine'], self.medicine)

    def test_cart_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/cart.html')

    def test_cart_view_unauthenticated(self):
        response = self.client.get(reverse('main:cart'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('main:add_to_cart', kwargs={'medicine_id': self.medicine.pk}),
            {'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if item was added to cart
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, medicine=self.medicine)
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='testpass123')
        # First add item to cart
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            medicine=self.medicine,
            quantity=1
        )
        
        response = self.client.post(
            reverse('main:remove_from_cart', kwargs={'item_id': cart_item.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if item was removed
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(pk=cart_item.pk)

    def test_add_review(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('main:add_review'),
            {
                'rating': 5,
                'text': 'Great service!'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if review was created
        review = Review.objects.get(user=self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, 'Great service!')

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')

    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/order_history.html')

class AuthenticationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer_group = Group.objects.create(name='Customers')

    def test_login_view(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')

        # Test login with correct credentials
        response = self.client.post(reverse('main:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Test login with incorrect credentials
        response = self.client.post(reverse('main:login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page

    def test_register_view(self):
        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/register.html')

        # Test registration with valid data
        response = self.client.post(reverse('main:register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if user was created and added to Customers group
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user.groups.filter(name='Customers').exists())

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout 