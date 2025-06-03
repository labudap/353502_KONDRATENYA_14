from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Sum, F, FloatField
from django.db.models.functions import ExtractYear
from statistics import mean, median, mode
from collections import Counter
from .models import (
    Medicine, Category, News, Glossary, Employee,
    CompanyInfo, JobVacancy, Review, Promo, Sale, Cart, CartItem, Profile, SaleItem, Department
)
from .forms import CustomUserCreationForm, MedicineForm, ReviewForm
from .decorators import employee_required, customer_required
from django.contrib.auth.models import Group, User
from datetime import datetime
from .calendar_utils import RussianCalendar
from .utils import get_cat_fact, get_activity
from .chart_utils import (
    get_sales_by_date_chart,
    get_category_sales_pie_chart,
    get_age_distribution_chart,
    get_top_medicines_bar_chart
)

def home(request):
    # Получаем параметры года и месяца из запроса
    try:
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
    except (ValueError, TypeError):
        year = datetime.now().year
        month = datetime.now().month
    
    # Создаем экземпляр календаря
    calendar_instance = RussianCalendar(year, month)
    calendar_data = calendar_instance.get_month_data()
    
    return render(request, 'main/home.html', {
        'calendar': calendar_data
    })

def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'main/about.html', {'company_info': company_info})

def news_list(request):
    news = News.objects.order_by('-date_published')
    return render(request, 'main/news_list.html', {'news': news})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'main/news_detail.html', {'news': news})

def glossary(request):
    terms = Glossary.objects.order_by('term')
    return render(request, 'main/glossary.html', {'terms': terms})

def contacts(request):
    # Получаем все отделы и их сотрудников
    departments = Department.objects.prefetch_related('employee_set').all()
    
    # Создаем словарь для группировки сотрудников по отделам
    departments_with_employees = []
    for department in departments:
        departments_with_employees.append({
            'department': department,
            'employees': department.employee_set.all()
        })
    
    return render(request, 'main/contacts.html', {
        'departments_with_employees': departments_with_employees
    })

def privacy(request):
    return render(request, 'main/privacy.html')

def vacancies(request):
    active_vacancies = JobVacancy.objects.filter(is_active=True)
    return render(request, 'main/vacancies.html', {'vacancies': active_vacancies})

def reviews(request):
    """Отображение списка отзывов"""
    reviews = Review.objects.select_related('user').order_by('-date')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('main:reviews')
    else:
        form = ReviewForm()
    
    return render(request, 'main/reviews.html', {
        'reviews': reviews,
        'form': form
    })

def promotions(request):
    active_promos = Promo.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now()
    )
    return render(request, 'main/promotions.html', {'promotions': active_promos})

def medicine_list(request):
    medicines = Medicine.objects.all()
    categories = Category.objects.filter(
        name__in=['Pain Relief', 'Supplements', 'Prescription']
    ).order_by('name')
    
    # Filter by category
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        medicines = medicines.filter(category_id__in=selected_categories)
    
    # Search by name
    search_query = request.GET.get('search', '').strip()
    search_error = None
    
    if search_query:
        if len(search_query) < 3:
            search_error = "Please enter at least 3 characters for search"
        else:
            # Поиск по имени и описанию
            medicines = medicines.filter(
                name__icontains=search_query
            ) | medicines.filter(
                description__icontains=search_query
            )
            medicines = medicines.distinct()  # Убираем дубликаты
    
    return render(request, 'main/medicine_list.html', {
        'medicines': medicines,
        'categories': categories,
        'selected_categories': selected_categories,
        'search_query': search_query,
        'search_error': search_error
    })

def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'main/medicine_detail.html', {'medicine': medicine})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    medicines = Medicine.objects.filter(category=category)
    return render(request, 'main/category_detail.html', {
        'category': category,
        'medicines': medicines
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Получаем тип аккаунта из формы
            account_type = form.cleaned_data.get('account_type')
            
            try:
                # Добавляем пользователя в соответствующую группу
                if account_type == 'employee':
                    group = Group.objects.get(name='Employees')
                    # Устанавливаем статус персонала для сотрудников
                    user.is_staff = True
                    user.save()
                    messages.success(request, f'Created employee account for {user.username} with staff status')
                else:
                    group = Group.objects.get(name='Customers')
                    messages.success(request, f'Created customer account for {user.username}')
                
                user.groups.add(group)
                messages.info(request, f'Added {user.username} to group {group.name}')
                
                # Проверяем, что пользователь действительно добавлен в группу
                if user.groups.filter(name=group.name).exists():
                    messages.info(request, f'Confirmed: {user.username} is in group {group.name}')
                else:
                    messages.warning(request, f'Warning: {user.username} was not added to group {group.name}')
                
            except Group.DoesNotExist:
                messages.error(request, f'Error: Group {account_type} does not exist')
            except Exception as e:
                messages.error(request, f'Error adding user to group: {str(e)}')
            
            # Автоматически входим в систему
            login(request, user)
            return redirect('main:home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        if phone:
            profile.phone = phone
        if address:
            profile.address = address
            
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('main:profile')
    
    user_orders = Sale.objects.filter(customer=request.user).order_by('-date')
    return render(request, 'main/profile.html', {
        'profile': profile,
        'orders': user_orders
    })

@login_required
def delete_review(request, review_id):
    """Удаление отзыва"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Отзыв успешно удален')
    return redirect('main:reviews')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.get_total_price()
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        if item_id and action:
            try:
                item = CartItem.objects.get(id=item_id, cart=cart)
                if action == 'remove':
                    item.delete()
                    messages.success(request, 'Item removed from cart.')
                elif action == 'update':
                    quantity = int(request.POST.get('quantity', 1))
                    if quantity > 0 and quantity <= item.medicine.stock:
                        item.quantity = quantity
                        item.save()
                        messages.success(request, 'Cart updated.')
                    else:
                        messages.error(request, 'Invalid quantity.')
            except CartItem.DoesNotExist:
                messages.error(request, 'Item not found.')
        
        return redirect('main:cart')
    
    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('main:cart')
    
    if request.method == 'POST':
        # Проверяем наличие товаров
        for item in cart_items:
            if item.quantity > item.medicine.stock:
                messages.error(request, f'Sorry, {item.medicine.name} only has {item.medicine.stock} items in stock.')
                return redirect('main:cart')
        
        # Создаем заказ
        total_amount = cart.get_total_price()
        sale = Sale.objects.create(
            customer=request.user,
            total_amount=total_amount
        )
        
        # Добавляем товары в заказ
        for item in cart_items:
            SaleItem.objects.create(
                sale=sale,
                medicine=item.medicine,
                quantity=item.quantity,
                price=item.medicine.price
            )
            # Уменьшаем количество товара на складе
            item.medicine.stock -= item.quantity
            item.medicine.save()
        
        # Очищаем корзину
        cart.items.all().delete()
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('main:order_detail', pk=sale.id)
    
    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'total_price': cart.get_total_price()
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Sale, pk=pk, customer=request.user)
    return render(request, 'main/order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Sale.objects.filter(customer=request.user).order_by('-date')
    return render(request, 'main/order_history.html', {'orders': orders})

@login_required
@customer_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0 and quantity <= medicine.stock:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                medicine=medicine,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            messages.success(request, f'Added {quantity} x {medicine.name} to your cart.')
        else:
            messages.error(request, 'Invalid quantity.')
    
    return redirect('main:medicine_detail', pk=medicine_id)

@employee_required
def sales_list(request):
    """View for employees to see all sales"""
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'main/sales_list.html', {'sales': sales})

@employee_required
def sale_detail(request, pk):
    """View for employees to see details of a specific sale"""
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'main/sale_detail.html', {'sale': sale})

@login_required
@employee_required
def medicine_create(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine = form.save()
            messages.success(request, f'Medicine "{medicine.name}" has been created successfully.')
            return redirect('main:medicine_detail', pk=medicine.id)
    else:
        form = MedicineForm()
    
    return render(request, 'main/medicine_form.html', {
        'form': form,
        'title': 'Add New Medicine',
        'button_text': 'Create Medicine'
    })

@login_required
@employee_required
def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            medicine = form.save()
            messages.success(request, f'Medicine "{medicine.name}" has been updated successfully.')
            return redirect('main:medicine_detail', pk=medicine.id)
    else:
        form = MedicineForm(instance=medicine)
    
    return render(request, 'main/medicine_form.html', {
        'form': form,
        'medicine': medicine,
        'title': 'Edit Medicine',
        'button_text': 'Update Medicine'
    })

@login_required
@employee_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        name = medicine.name
        medicine.delete()
        messages.success(request, f'Medicine "{name}" has been deleted successfully.')
        return redirect('main:medicine_list')
    
    return render(request, 'main/medicine_confirm_delete.html', {
        'medicine': medicine
    })

def fun_corner(request):
    """
    View for fun corner page with cat facts and activity suggestions
    """
    # Get a random cat fact
    cat_fact = get_cat_fact()
    
    # Get a random activity suggestion
    activity = get_activity()
    
    context = {
        'cat_fact': cat_fact,
        'activity': activity
    }
    return render(request, 'main/fun_corner.html', context)

@login_required
@employee_required
def statistics(request):
    """View for pharmacy statistics"""
    
    # Получаем всех клиентов (пользователей из группы Customers)
    customers_group = Group.objects.get(name='Customers')
    customers = User.objects.filter(groups=customers_group).order_by('username')
    
    # Статистика по продажам
    sales_data = Sale.objects.aggregate(
        total_sales=Sum('total_amount'),
        avg_sale=Avg('total_amount')
    )
    
    # Получаем все суммы продаж для расчета медианы и моды
    all_sales = list(Sale.objects.values_list('total_amount', flat=True))
    sales_median = median(all_sales) if all_sales else 0
    sales_mode = mode(all_sales) if all_sales else 0
    
    # Статистика по возрасту клиентов
    current_year = datetime.now().year
    profiles_with_age = Profile.objects.exclude(date_of_birth=None).annotate(
        age=current_year - ExtractYear('date_of_birth')
    )
    
    age_stats = {
        'avg_age': profiles_with_age.aggregate(Avg('age'))['age__avg'] or 0,
        'median_age': median([p.age for p in profiles_with_age]) if profiles_with_age else 0
    }
    
    # Статистика по типам товаров (категориям)
    category_stats = SaleItem.objects.values(
        'medicine__category__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'), output_field=FloatField())
    ).order_by('-total_quantity')
    
    # Список товаров в алфавитном порядке с общей суммой продаж
    medicines_stats = Medicine.objects.annotate(
        total_sales=Sum(F('saleitem__quantity') * F('saleitem__price'), output_field=FloatField())
    ).order_by('name')
    
    # Генерируем только нужные графики
    category_chart = get_category_sales_pie_chart(SaleItem.objects)
    top_medicines_chart = get_top_medicines_bar_chart(SaleItem.objects)
    
    context = {
        'customers': customers,
        'total_customers': customers.count(),
        'sales_stats': {
            'total_sales': sales_data['total_sales'] or 0,
            'avg_sale': sales_data['avg_sale'] or 0,
            'median_sale': sales_median,
            'mode_sale': sales_mode
        },
        'age_stats': age_stats,
        'category_stats': category_stats,
        'medicines_stats': medicines_stats,
        'charts': {
            'category_chart': category_chart,
            'top_medicines_chart': top_medicines_chart
        }
    }
    
    return render(request, 'main/statistics.html', context)
