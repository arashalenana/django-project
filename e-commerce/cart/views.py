from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from .models import CartItem
# Create your views here.
@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.subtotal for item in items)
    return render(request, 'cart/cart.html', {'items': items, 'total': total})


@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(
        user=request.user, product=product, defaults={'quantity': 1}
    )
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart:view')


@login_required
@require_POST
def cart_update(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            messages.info(request, 'Item removed from cart.')
        else:
            item.save()

    return redirect('cart:view')


@login_required
@require_POST
def cart_remove(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('cart:view')