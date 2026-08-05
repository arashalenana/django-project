from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .decorators import staff_required, dashboard_permission_required, superuser_required
from django.views.decorators.http import require_POST
from .forms import (
    DashboardProductForm, DashboardCategoryForm,
    DashboardUserPermissionsForm, DashboardOrderStatusForm,
)
from django.contrib.auth import get_user_model
from products.models import Product, Category
from orders.models import Order
from .decorators import staff_required
# Create your views here.
User = get_user_model()

@staff_required
def dashboard_home(request):
    products_qs = Product.objects.all()
    total_products = products_qs.count()
    available_products = products_qs.filter(is_available=True, stock_quantity__gt=0).count()
    out_of_stock_products = products_qs.filter(stock_quantity=0).count()

    total_categories = Category.objects.count()
    total_profiles = User.objects.count()

    orders_qs = Order.objects.all()
    total_orders = orders_qs.count()
    
    pending_orders = orders_qs.filter(status='pending').count()
    delivered_orders = orders_qs.filter(status='delivered').count()

    recent_orders = orders_qs.select_related('user').order_by('-date_created')[:5]
    recent_products = products_qs.select_related('category').order_by('-date_created')[:5]

    context = {
        'total_products': total_products,
        'available_products': available_products,
        'out_of_stock_products': out_of_stock_products,
        'total_categories': total_categories,
        'total_profiles': total_profiles,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }
    return render(request, 'dashboard/dashboard_home.html', context)

# Products
@dashboard_permission_required('products.view_product')
def product_list(request):
    products = Product.objects.select_related('category').all().order_by('-date_created')

    query = request.GET.get('q', '')
    if query:
        products = products.filter(name__icontains=query)

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    availability = request.GET.get('availability', '')
    if availability == 'available':
        products = products.filter(is_available=True)
    elif availability == 'unavailable':
        products = products.filter(is_available=False)

    stock_status = request.GET.get('stock', '')
    if stock_status == 'in_stock':
        products = products.filter(stock_quantity__gt=0)
    elif stock_status == 'out_of_stock':
        products = products.filter(stock_quantity=0)

    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'active_section': 'products',
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'query': query,
        'selected_category': category_id,
        'selected_availability': availability,
        'selected_stock': stock_status,
    }
    return render(request, 'dashboard/products/product_list.html', context)

@dashboard_permission_required('products.add_product')
def product_add(request):
    if request.method == 'POST':
        form = DashboardProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('dashboard:product_list')
    else:
        form = DashboardProductForm()

    return render(request, 'dashboard/products/product_form.html', {
        'active_section': 'products', 'form': form, 'is_edit': False,
    })

@dashboard_permission_required('products.change_product')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = DashboardProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('dashboard:product_list')
    else:
        form = DashboardProductForm(instance=product)

    return render(request, 'dashboard/products/product_form.html', {
        'active_section': 'products', 'form': form, 'is_edit': True, 'product': product,
    })


@dashboard_permission_required('products.delete_product')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('dashboard:product_list')

    return render(request, 'dashboard/products/product_confirm_delete.html', {
        'active_section': 'products', 'product': product,
    })

# Categories
@dashboard_permission_required('products.view_category')
def category_list(request):
    categories = Category.objects.all().order_by('name')

    query = request.GET.get('q', '')
    if query:
        categories = categories.filter(name__icontains=query)

    categories = categories.prefetch_related('products')

    paginator = Paginator(categories, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'dashboard/categories/category_list.html', {
        'active_section': 'categories', 'page_obj': page_obj, 'query': query,
    })


@dashboard_permission_required('products.add_category')
def category_add(request):
    if request.method == 'POST':
        form = DashboardCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('dashboard:category_list')
    else:
        form = DashboardCategoryForm()

    return render(request, 'dashboard/categories/category_form.html', {
        'active_section': 'categories', 'form': form, 'is_edit': False,
    })

@dashboard_permission_required('products.change_category')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = DashboardCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('dashboard:category_list')
    else:
        form = DashboardCategoryForm(instance=category)

    return render(request, 'dashboard/categories/category_form.html', {
        'active_section': 'categories', 'form': form, 'is_edit': True, 'category': category,
    })

@dashboard_permission_required('products.delete_category')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    product_count = category.products.count()

    if request.method == 'POST':
        if product_count > 0:
            messages.error(
                request,
                f'Cannot delete "{category.name}" because it still has {product_count} '
                f'product(s). Move or delete those products first.'
            )
            return redirect('dashboard:category_list')
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('dashboard:category_list')

    return render(request, 'dashboard/categories/category_confirm_delete.html', {
        'active_section': 'categories', 'category': category, 'product_count': product_count,
    })

# Profiles
@dashboard_permission_required('authentication.view_user')
def profile_list(request):
    profiles = User.objects.all().order_by('-date_joined')

    query = request.GET.get('q', '')
    if query:
        profiles = profiles.filter(Q(username__icontains=query) | Q(email__icontains=query))

    account_type = request.GET.get('type', '')
    if account_type == 'superuser':
        profiles = profiles.filter(is_superuser=True)
    elif account_type == 'staff':
        profiles = profiles.filter(is_staff=True, is_superuser=False)
    elif account_type == 'customer':
        profiles = profiles.filter(is_staff=False)

    active_status = request.GET.get('active', '')
    if active_status == 'active':
        profiles = profiles.filter(is_active=True)
    elif active_status == 'inactive':
        profiles = profiles.filter(is_active=False)

    paginator = Paginator(profiles, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'dashboard/profiles/profile_list.html', {
        'active_section': 'profiles', 'page_obj': page_obj, 'query': query,
        'selected_type': account_type, 'selected_active': active_status,
    })

@dashboard_permission_required('authentication.view_user')
def profile_detail(request, pk):
    profile = get_object_or_404(User, pk=pk)
    recent_orders = Order.objects.filter(user=profile).order_by('-date_created')[:10]

    return render(request, 'dashboard/profiles/profile_detail.html', {
        'active_section': 'profiles', 'profile_user': profile, 'recent_orders': recent_orders,
    })

def _is_last_active_superuser(target_user):
    if not target_user.is_superuser or not target_user.is_active:
        return False
    other_active_superusers = User.objects.filter(
        is_superuser=True, is_active=True
    ).exclude(pk=target_user.pk)
    return not other_active_superusers.exists()

# Settings
@superuser_required
def settings_list(request):
    accounts = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/settings/account_settings.html', {
        'active_section': 'settings', 'accounts': accounts,
    })


@superuser_required
@require_POST
def settings_promote(request, pk):
    target = get_object_or_404(User, pk=pk)
    target.is_staff = True
    target.save(update_fields=['is_staff'])
    messages.success(request, f'{target.username} has been granted dashboard access.')
    return redirect('dashboard:settings_list')


@superuser_required
def settings_demote(request, pk):
    target = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if target.is_superuser and _is_last_active_superuser(target):
            messages.error(
                request,
                'Cannot demote this account: it is the last active superuser. '
                'Promote another account to superuser first.'
            )
            return redirect('dashboard:settings_list')

        target.is_staff = False
        target.save(update_fields=['is_staff'])
        messages.success(request, f'{target.username} has been demoted and no longer has dashboard access.')
        return redirect('dashboard:settings_list')

    return render(request, 'dashboard/settings/demote_confirm.html', {
        'active_section': 'settings', 'target': target,
    })


@superuser_required
@require_POST
def settings_toggle_active(request, pk):
    target = get_object_or_404(User, pk=pk)

    if target.is_active and _is_last_active_superuser(target):
        messages.error(
            request,
            'Cannot deactivate this account: it is the last active superuser.'
        )
        return redirect('dashboard:settings_list')

    target.is_active = not target.is_active
    target.save(update_fields=['is_active'])
    state = 'activated' if target.is_active else 'deactivated'
    messages.success(request, f'{target.username} has been {state}.')
    return redirect('dashboard:settings_list')


@superuser_required
def settings_permissions(request, pk):
    target = get_object_or_404(User, pk=pk)

    if target.is_superuser and target != request.user:
        messages.info(request, 'Superuser accounts already have every permission implicitly.')

    if request.method == 'POST':
        form = DashboardUserPermissionsForm(request.POST)
        if form.is_valid():
            target.user_permissions.set(form.cleaned_data['permissions'])
            messages.success(request, f'Permissions updated for {target.username}.')
            return redirect('dashboard:settings_list')
    else:
        form = DashboardUserPermissionsForm(initial={'permissions': target.user_permissions.all()})

    return render(request, 'dashboard/settings/permissions_form.html', {
        'active_section': 'settings', 'target': target, 'form': form,
    })

# Order
@dashboard_permission_required('orders.view_order')
def order_list(request):
    orders = Order.objects.select_related('user').all().order_by('-date_created')

    query = request.GET.get('q', '')
    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(full_name__icontains=query) |
            Q(email__icontains=query)
        )

    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)

    paginator = Paginator(orders, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'dashboard/orders/order_list.html', {
        'active_section': 'orders', 'page_obj': page_obj, 'query': query,
        'selected_status': status, 'status_choices': Order.STATUS_CHOICES,
    })

@dashboard_permission_required('orders.view_order')
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('user'), pk=pk)
    items = order.items.select_related('product')

    status_form = DashboardOrderStatusForm(instance=order)

    return render(request, 'dashboard/orders/order_detail.html', {
        'active_section': 'orders', 'order': order, 'items': items, 'status_form': status_form,
    })

@dashboard_permission_required('orders.change_order')
@require_POST
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = DashboardOrderStatusForm(request.POST, instance=order)
    if form.is_valid():
        form.save()
        messages.success(request, 'Order status updated successfully.')
    else:
        messages.error(request, 'Could not update order status. Please try again.')
    return redirect('dashboard:order_detail', pk=order.pk)