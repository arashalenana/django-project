from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('search/', views.product_search, name='search'),
    path('category/<slug:slug>/', views.product_category, name='category'),
    path('<slug:slug>/', views.product_detail, name='detail'),
]