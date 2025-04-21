from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from store.models import Product
from users.models import CustomUser, UserAddress, UserSecondaryAddress
from cart.models import ShoppingSession, CartItem
from django.http import HttpResponse
from django.http import JsonResponse


@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)

    session, _ = ShoppingSession.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(session=session, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # 👇 Check if it's an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(f'"{product.name}" has been added to your cart.')

    # Else redirect like normal
    return redirect('cart:view_cart')


@login_required
def view_cart(request):
    user = request.user
    session = ShoppingSession.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(session=session) if session else []
    cart_total = sum(item.subtotal for item in cart_items)
    
    # Fetch user primary and secondary addresses
    user_addresses = UserAddress.objects.filter(user=user)
    user_secondary_addresses = UserSecondaryAddress.objects.filter(user=user)
    
    address_count = user_addresses.count()  # Primary address count
    secondary_address_count = user_secondary_addresses.count()  # Secondary address count

    # Show Add Another Address button only if there's a primary address and no secondary address
    show_add_address_button = address_count > 0 and secondary_address_count == 0

    return render(request, 'cart/view_cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user_addresses': user_addresses,
        'user_secondary_addresses': user_secondary_addresses,  # Add secondary addresses
        'address_count': address_count,
        'secondary_address_count': secondary_address_count,
        'show_add_address_button': show_add_address_button,  # Add the variable for the button visibility
    })



@require_POST
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, session__user=request.user)

    action = request.POST.get('action')
    quantity = item.quantity

    if action == 'increase':
        quantity += 1
    elif action == 'decrease':
        quantity = max(1, quantity - 1)
    else:
        # For manual input
        try:
            quantity = int(request.POST.get('quantity', 1))
            quantity = max(1, quantity)
        except (ValueError, TypeError):
            quantity = 1

    item.quantity = quantity
    item.save()
    return redirect('cart:view_cart')

@require_POST
@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, session__user=request.user)
    item.delete()
    return redirect('cart:view_cart')