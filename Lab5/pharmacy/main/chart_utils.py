import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid display issues
import io
import base64
from datetime import datetime, timedelta
import numpy as np
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

def get_sales_by_date_chart(sales_queryset):
    """Generate line chart for sales over time"""
    plt.clf()  # Clear the current figure
    
    # Получаем данные о продажах по датам за последние 30 дней
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    sales_by_date = sales_queryset.filter(
        date__range=[start_date, end_date]
    ).annotate(
        sale_date=TruncDate('date')
    ).values('sale_date').annotate(
        total=Sum('total_amount')
    ).order_by('sale_date')
    
    dates = [item['sale_date'] for item in sales_by_date]
    totals = [float(item['total']) for item in sales_by_date]
    
    if not dates:  # Если нет данных, возвращаем пустой график
        plt.plot([], [])
        plt.title('No sales data available')
    else:
        plt.figure(figsize=(10, 5))
        plt.plot(dates, totals, marker='o')
        plt.title('Sales Over Last 30 Days')
        plt.xlabel('Date')
        plt.ylabel('Total Sales (₽)')
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode()

def get_category_sales_pie_chart(sale_items_queryset):
    """Generate pie chart for sales distribution by category"""
    plt.clf()
    
    # Получаем данные о продажах по категориям
    category_sales = sale_items_queryset.values(
        'medicine__category__name'
    ).annotate(
        total=Sum('price')
    ).order_by('-total')
    
    categories = [item['medicine__category__name'] for item in category_sales]
    totals = [float(item['total']) for item in category_sales]
    
    if not categories:
        plt.pie([1], labels=['No data'])
        plt.title('No category data available')
    else:
        plt.figure(figsize=(8, 8))
        plt.pie(totals, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title('Sales Distribution by Category')
        plt.axis('equal')
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode()

def get_age_distribution_chart(profiles_queryset):
    """Generate histogram for customer age distribution"""
    plt.clf()
    
    # Получаем возраст всех клиентов
    current_year = datetime.now().year
    ages = [
        current_year - profile.date_of_birth.year
        for profile in profiles_queryset
        if profile.date_of_birth
    ]
    
    if not ages:
        plt.hist([], bins=[])
        plt.title('No age data available')
    else:
        plt.figure(figsize=(8, 5))
        plt.hist(ages, bins=range(min(ages), max(ages) + 2, 5), 
                edgecolor='black', alpha=0.7)
        plt.title('Customer Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Number of Customers')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode()

def get_top_medicines_bar_chart(sale_items_queryset):
    """Generate bar chart for top 10 selling medicines"""
    plt.clf()
    
    # Получаем топ-10 лекарств по количеству продаж
    top_medicines = sale_items_queryset.values(
        'medicine__name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:10]
    
    medicines = [item['medicine__name'] for item in top_medicines]
    quantities = [item['total_quantity'] for item in top_medicines]
    
    if not medicines:
        plt.bar([], [])
        plt.title('No medicine sales data available')
    else:
        plt.figure(figsize=(10, 5))
        bars = plt.bar(range(len(medicines)), quantities)
        plt.title('Top 10 Selling Medicines')
        plt.xlabel('Medicine Name')
        plt.ylabel('Total Quantity Sold')
        plt.xticks(range(len(medicines)), medicines, rotation=45, ha='right')
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode() 