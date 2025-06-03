from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Department, Category, Supplier, Employee, Medicine,
    MedicineSupplier, Sale, SaleItem, Promo, Review,
    CompanyInfo, News, Glossary, JobVacancy,
    Cart, CartItem, Profile
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person', 'email')
    list_filter = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'phone')
    list_filter = ('department', 'position')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'position')
    raw_id_fields = ('user',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(MedicineSupplier)
class MedicineSupplierAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'supplier', 'supply_price', 'last_supply_date')
    list_filter = ('supplier', 'last_supply_date')
    search_fields = ('medicine__name', 'supplier__name')

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date', 'total_amount')
    list_filter = ('date',)
    search_fields = ('customer__username',)
    inlines = [SaleItemInline]

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('user__username', 'text')

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published')
    list_filter = ('date_published',)
    search_fields = ('title', 'content')

@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    list_display = ('term', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('term', 'definition')

@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'medicine', 'quantity')
    list_filter = ('cart', 'medicine')
    search_fields = ('cart__user__username', 'medicine__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone', 'address')

# Настраиваем отображение пользователей
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'

# Перерегистрируем модель User с нашим CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
