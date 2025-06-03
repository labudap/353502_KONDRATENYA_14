from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('glossary/', views.glossary, name='glossary'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('fun-corner/', views.fun_corner, name='fun_corner'),
    path('promotions/', views.promotions, name='promotions'),
    
    # Medicine related
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('medicines/create/', views.medicine_create, name='medicine_create'),
    path('medicines/<int:pk>/update/', views.medicine_update, name='medicine_update'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('medicines/<int:medicine_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    
    # User related
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Shopping related
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    
    # Новые URL-маршруты для сотрудников
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('statistics/', views.statistics, name='statistics'),
] 