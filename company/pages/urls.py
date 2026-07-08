from django.urls import path
from .views import home_page_view, AboutPageView
urlpatterns=[
    path('abouts/', AboutPageView.as_view(), name='about'),
    path('', home_page_view, name='home')
]