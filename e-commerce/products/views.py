from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import TemplateView
from .models import Product, Category

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_available=True)[:8]
        context['categories'] = Category.objects.all()[:6]
        return context


def product_list(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})


def product_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_available=True)
    return render(request, 'products/product_category.html', {
        'category': category,
        'products': products,
    })


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_available=True)
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'products/product_search.html', {
        'products': products,
        'query': query,
    })