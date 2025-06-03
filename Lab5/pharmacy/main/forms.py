from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from datetime import date
from .models import Profile, Medicine, Review
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message='Enter a valid email address. For example: user@example.com'
            )
        ],
        widget=forms.EmailInput(attrs={
            'placeholder': 'user@example.com',
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        }),
        help_text='Enter a valid email address in format: user@example.com'
    )
    ACCOUNT_TYPES = [
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    ]
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES, required=True, label='Account Type')
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date of Birth'
    )
    phone = forms.CharField(
        max_length=19,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Phone number must be in format: +375 (29) XXX-XX-XX'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': '+375 (29) XXX-XX-XX',
            'pattern': r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$'
        }),
        help_text='Enter phone number in format: +375 (29) XXX-XX-XX'
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "account_type", "date_of_birth", "phone"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        account_type = self.cleaned_data.get('account_type')
        
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            
            if account_type == 'employee':
                if age < 18 or age > 45:
                    raise forms.ValidationError('Employees must be between 18 and 45 years old.')
            else:
                if age < 18:
                    raise forms.ValidationError('Customers must be at least 18 years old.')
        
        return date_of_birth

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            # Создаем профиль пользователя с датой рождения и телефоном
            profile = Profile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data["date_of_birth"],
                phone=self.cleaned_data["phone"]
            )
        
        return user 

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'instructions', 'price', 'stock', 'category', 'code', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 4}),
        } 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'rating': 'Оценка',
            'text': 'Ваш отзыв'
        } 