from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from main.models import Medicine, Sale, Employee, Cart, CartItem, Review

class Command(BaseCommand):
    help = 'Create default groups and permissions'

    def handle(self, *args, **options):
        # Create groups
        employee_group, _ = Group.objects.get_or_create(name='Employees')
        customer_group, _ = Group.objects.get_or_create(name='Customers')

        # Get content types
        medicine_ct = ContentType.objects.get_for_model(Medicine)
        sale_ct = ContentType.objects.get_for_model(Sale)
        employee_ct = ContentType.objects.get_for_model(Employee)
        cart_ct = ContentType.objects.get_for_model(Cart)
        cart_item_ct = ContentType.objects.get_for_model(CartItem)
        review_ct = ContentType.objects.get_for_model(Review)

        # Permissions for employees
        employee_permissions = [
            # Medicine permissions
            Permission.objects.get(content_type=medicine_ct, codename='view_medicine'),
            Permission.objects.get(content_type=medicine_ct, codename='add_medicine'),
            Permission.objects.get(content_type=medicine_ct, codename='change_medicine'),
            Permission.objects.get(content_type=medicine_ct, codename='delete_medicine'),
            # Sale permissions
            Permission.objects.get(content_type=sale_ct, codename='view_sale'),
            Permission.objects.get(content_type=sale_ct, codename='add_sale'),
            Permission.objects.get(content_type=sale_ct, codename='change_sale'),
            Permission.objects.get(content_type=sale_ct, codename='delete_sale'),
            # Employee permissions
            Permission.objects.get(content_type=employee_ct, codename='view_employee'),
            Permission.objects.get(content_type=employee_ct, codename='add_employee'),
            Permission.objects.get(content_type=employee_ct, codename='change_employee'),
            Permission.objects.get(content_type=employee_ct, codename='delete_employee'),
        ]

        # Permissions for customers
        customer_permissions = [
            Permission.objects.get(content_type=medicine_ct, codename='view_medicine'),
            Permission.objects.get(content_type=cart_ct, codename='add_cart'),
            Permission.objects.get(content_type=cart_ct, codename='view_cart'),
            Permission.objects.get(content_type=cart_ct, codename='change_cart'),
            Permission.objects.get(content_type=cart_item_ct, codename='add_cartitem'),
            Permission.objects.get(content_type=cart_item_ct, codename='view_cartitem'),
            Permission.objects.get(content_type=cart_item_ct, codename='change_cartitem'),
            Permission.objects.get(content_type=cart_item_ct, codename='delete_cartitem'),
            Permission.objects.get(content_type=review_ct, codename='add_review'),
            Permission.objects.get(content_type=review_ct, codename='view_review'),
        ]

        # Clear existing permissions and add new ones
        employee_group.permissions.clear()
        employee_group.permissions.add(*employee_permissions)

        customer_group.permissions.clear()
        customer_group.permissions.add(*customer_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions')) 