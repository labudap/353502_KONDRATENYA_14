from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from datetime import date

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Phone number must be in format: +375 (29) XXX-XX-XX'
            )
        ]
    )
    email = models.EmailField()
    address = models.TextField()
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Phone number must be in format: +375 (29) XXX-XX-XX'
            )
        ]
    )
    position = models.CharField(max_length=100)
    job_description = models.TextField(
        help_text="Detailed description of employee's responsibilities",
        null=True,
        blank=True
    )
    email = models.EmailField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message='Enter a valid email address'
            )
        ],
        null=True,
        blank=True
    )
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='employees/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            age = (timezone.now().date() - self.date_of_birth).days // 365
            if age < 18:
                raise ValueError("Employee must be 18 or older")
        super().save(*args, **kwargs)

class Medicine(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    suppliers = models.ManyToManyField(Supplier)
    image = models.ImageField(upload_to='medicines/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class MedicineSupplier(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supply_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_supply_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('medicine', 'supplier')

class Sale(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Sale {self.id} - {self.date.strftime('%d/%m/%Y')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Promo(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"

class CompanyInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    history = models.TextField()
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Company Info"
    
    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "News"
    
    def __str__(self):
        return self.title

class Glossary(models.Model):
    term = models.CharField(max_length=200)
    definition = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Glossary"
    
    def __str__(self):
        return self.term

class JobVacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Job Vacancies"
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.name}"

    def get_cost(self):
        return self.medicine.price * self.quantity

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Phone number must be in format: +375 (29) XXX-XX-XX'
            )
        ],
        null=True,
        blank=True
    )
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

    def get_age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date_of_birth:
            age = self.get_age()
            # Проверяем, является ли пользователь сотрудником
            is_employee = self.user.groups.filter(name='Employees').exists()
            
            if is_employee:
                if age < 18 or age > 45:
                    raise ValidationError('Employees must be between 18 and 45 years old.')
            else:
                if age < 18:
                    raise ValidationError('Customers must be at least 18 years old.')
