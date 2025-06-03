def user_role(request):
    """
    Добавляет информацию о роли пользователя в контекст шаблона
    """
    context = {
        'is_employee': False,
        'is_customer': False
    }
    
    if request.user.is_authenticated:
        if request.user.is_staff and request.user.groups.filter(name='Employees').exists():
            context['is_employee'] = True
        elif request.user.groups.filter(name='Customers').exists():
            context['is_customer'] = True
    
    return context 