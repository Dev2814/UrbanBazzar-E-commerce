from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserAddress, UserSecondaryAddress
from cart.models import CartItem, ShoppingSession
from orders.models import OrderDetails, OrderItems
from payments.models import PaymentDetails
from store.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.http import require_POST

def send_order_confirmation_email(user, order, payment_method):
    email_subject = '🛍️ Your Order Confirmation - UrbanBazzar'
    email_context = {
        'firstname': user.first_name,
        'order_number': order.id,
        'total_amount': order.total,
        'shipping_address': f"{order.address}, {order.city}, {order.pincode}, {order.country}",
        'payment_method': payment_method.upper(),
        'support_email': 'support@urbanbazzar.com',
        'help_center_url': 'http://127.0.0.1:2814/help/',
    }
    email_body = render_to_string('emails/order_place_email.html', email_context)

    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)


@login_required
def confirm_order(request):
    if request.method == "POST":
        address_id = request.POST.get('selected_address')
        payment_method = request.POST.get('payment_method')
        upi_id = request.POST.get('upi_id', '')

        if not address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('cart:view_cart')

        address_obj = (
            UserAddress.objects.filter(id=address_id, user=request.user).first() or
            UserSecondaryAddress.objects.filter(id=address_id, user=request.user).first()
        )

        if not address_obj:
            messages.error(request, "Invalid address selection.")
            return redirect('cart:view_cart')

        session = get_object_or_404(ShoppingSession, user=request.user)
        cart_items = CartItem.objects.filter(session=session)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('store:product_list')

        # Calculate total
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = OrderDetails.objects.create(
            user=request.user,
            address=address_obj.address,
            city=address_obj.city,
            pincode=address_obj.pincode,
            country=address_obj.country,
            mobile=address_obj.mobile,
            total=total_amount,
            payment=None
        )

        # Create order items & update stock
        for item in cart_items:
            OrderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save()

        # Create payment
        payment = PaymentDetails.objects.create(
            order=order,
            amount=total_amount,
            provider=payment_method,
            status="pending" if payment_method == "COD" else "processing",
        )

        order.payment = payment
        order.save()

        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        send_order_confirmation_email(request.user, order, payment_method)
        return redirect('orders:order_success')

    return redirect('cart:view_cart')



@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')

@login_required
def order_list(request):
    orders = OrderDetails.objects.filter(user=request.user).order_by('-created_at')
    for order in orders:
        for item in order.orderitems.all():  # This now works thanks to related_name
            item.line_total = item.product.price * item.quantity
    return render(request, 'orders/orders.html', {'orders': orders})
