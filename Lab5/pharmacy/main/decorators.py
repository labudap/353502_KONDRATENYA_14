from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def employee_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff and request.user.groups.filter(name='Employees').exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Employee privileges required.')
        return redirect('main:home')
    return _wrapped_view

def customer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Customers').exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Customer privileges required.')
        return redirect('main:home')
    return _wrapped_view 