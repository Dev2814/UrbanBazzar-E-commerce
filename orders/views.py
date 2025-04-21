# Import necessary Django modules and app models
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

# Function to send a confirmation email after a successful order
def send_order_confirmation_email(user, order, payment_method):
    email_subject = '🛍️ Your Order Confirmation - UrbanBazzar'  # Email subject line
    
    # Prepare email content with order details
    email_context = {
        'firstname': user.first_name,
        'order_number': order.id,
        'total_amount': order.total,
        'shipping_address': f"{order.address}, {order.city}, {order.pincode}, {order.country}",
        'payment_method': payment_method.upper(),
        'support_email': 'support@urbanbazzar.com',
        'help_center_url': 'http://127.0.0.1:2814/help/',
    }

    # Render HTML email body from template
    email_body = render_to_string('emails/order_place_email.html', email_context)

    # Create the email object and send it
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.content_subtype = "html"  # Specify content type as HTML
    email.send(fail_silently=False)  # Send the email, raise error if fails


# View to confirm and process an order from the cart
@login_required  # Ensures the user is logged in
def confirm_order(request):
    if request.method == "POST":  # Only allow POST requests
        address_id = request.POST.get('selected_address')  # Get selected address ID
        payment_method = request.POST.get('payment_method')  # Get selected payment method
        upi_id = request.POST.get('upi_id', '')  # Optional UPI ID

        # If no address is selected, show an error
        if not address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('cart:view_cart')

        # Try to fetch the selected primary or secondary address
        address_obj = (
            UserAddress.objects.filter(id=address_id, user=request.user).first() or
            UserSecondaryAddress.objects.filter(id=address_id, user=request.user).first()
        )

        # If address is not found, show an error
        if not address_obj:
            messages.error(request, "Invalid address selection.")
            return redirect('cart:view_cart')

        # Get the user's shopping session and cart items
        session = get_object_or_404(ShoppingSession, user=request.user)
        cart_items = CartItem.objects.filter(session=session)

        # If the cart is empty, redirect to products page
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('store:product_list')

        # Calculate total order amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create the order object
        order = OrderDetails.objects.create(
            user=request.user,
            address=address_obj.address,
            city=address_obj.city,
            pincode=address_obj.pincode,
            country=address_obj.country,
            mobile=address_obj.mobile,
            total=total_amount,
            payment=None  # Will be assigned after payment object is created
        )

        # Create order items and update product stock
        for item in cart_items:
            OrderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            item.product.stock -= item.quantity  # Decrease stock
            item.product.save()  # Save updated stock

        # Create a payment record for the order
        payment = PaymentDetails.objects.create(
            order=order,
            amount=total_amount,
            provider=payment_method,
            status="pending" if payment_method == "COD" else "processing",
        )

        # Link payment to order and save
        order.payment = payment
        order.save()

        # Clear the user's cart
        cart_items.delete()

        # Show success message and send confirmation email
        messages.success(request, "Order placed successfully!")
        send_order_confirmation_email(request.user, order, payment_method)
        return redirect('orders:order_success')  # Redirect to order success page

    # If not a POST request, redirect to cart
    return redirect('cart:view_cart')


# View to render the order success page
@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')  # Display success template


# View to list all orders placed by the user
@login_required
def order_list(request):
    # Get user's orders, most recent first
    orders = OrderDetails.objects.filter(user=request.user).order_by('-created_at')

    # Add line_total for each order item for display
    for order in orders:
        for item in order.orderitems.all():  # orderitems is accessible via related_name
            item.line_total = item.product.price * item.quantity

    # Render orders in template
    return render(request, 'orders/orders.html', {'orders': orders})
