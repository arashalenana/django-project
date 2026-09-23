from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm
from .services import make_payment, confirm_payment
# Create your views here.
@login_required
def checkout_view(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related('product')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:view')

    total = sum(item.subtotal for item in cart_items)

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            # -------------------------
            # MAKE M-PESA PAYMENT
            # -------------------------
            try:
                payment_response = make_payment(
                    request.user.phone_number,
                    total
                )

            except Exception as e:
                messages.error(
                    request,
                    f'Unable to initiate payment: {e}'
                )
                return redirect('cart:view')

            # -------------------------
            # CHECK STK PUSH RESPONSE
            # -------------------------
            if payment_response.get('ResponseCode') != '0':

                messages.error(
                    request,
                    payment_response.get(
                        'ResponseDescription',
                        'Payment request failed.'
                    )
                )

                return redirect('cart:view')

            # -------------------------
            # PAYMENT REQUEST ACCEPTED
            # -------------------------

            order = form.save(commit=False)

            order.user = request.user
            order.total_amount = total

            # Save the order
            order.save()

            # Create order items
            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.display_price
                )

            # Clear cart
            cart_items.delete()

            messages.success(
                request,
                'Payment request sent. Please complete the payment on your phone.'
            )

            return redirect(
                'orders:confirmation',
                order_number=order.order_number
            )

    else:

        initial = {
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
            'phone_number': request.user.phone_number,
            'delivery_address': request.user.address,
        }

        form = CheckoutForm(initial=initial)

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart_items': cart_items,
            'total': total,
        }
    )       

@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})