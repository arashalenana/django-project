from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('settings/', views.settings_list, name='settings_list'),
    path('settings/<int:pk>/promote/', views.settings_promote, name='settings_promote'),
    path('settings/<int:pk>/demote/', views.settings_demote, name='settings_demote'),
    path('settings/<int:pk>/toggle-active/', views.settings_toggle_active, name='settings_toggle_active'),
    path('settings/<int:pk>/permissions/', views.settings_permissions, name='settings_permissions'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/status/', views.order_update_status, name='order_update_status'),
]