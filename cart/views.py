# Import necessary Django modules and models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from store.models import Product
from users.models import CustomUser, UserAddress, UserSecondaryAddress
from cart.models import ShoppingSession, CartItem
from django.http import HttpResponse, JsonResponse

# View to add a product to the user's shopping cart
@login_required  # Ensures the user is logged in
def add_to_cart(request, product_id):
    user = request.user  # Get the current user
    product = get_object_or_404(Product, pk=product_id)  # Get the product or return 404

    # Get or create a shopping session for the user
    session, _ = ShoppingSession.objects.get_or_create(user=user)

    # Get or create a cart item for the selected product
    cart_item, created = CartItem.objects.get_or_create(session=session, product=product)
    
    # If the item already exists in the cart, increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Check if the request was made via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(f'"{product.name}" has been added to your cart.')

    # Otherwise, redirect the user to the cart view
    return redirect('cart:view_cart')

# View to display the current user's cart
@login_required  # Ensures the user is logged in
def view_cart(request):
    user = request.user  # Get the current user
    session = ShoppingSession.objects.filter(user=user).first()  # Get user's session
    cart_items = CartItem.objects.filter(session=session) if session else []  # Get items or empty list
    cart_total = sum(item.subtotal for item in cart_items)  # Calculate total cart value
    
    # Fetch user addresses (primary and secondary)
    user_addresses = UserAddress.objects.filter(user=user)
    user_secondary_addresses = UserSecondaryAddress.objects.filter(user=user)
    
    # Count addresses
    address_count = user_addresses.count()
    secondary_address_count = user_secondary_addresses.count()

    # Determine if "Add Another Address" button should be shown
    show_add_address_button = address_count > 0 and secondary_address_count == 0

    # Render the cart template with all the context data
    return render(request, 'cart/view_cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user_addresses': user_addresses,
        'user_secondary_addresses': user_secondary_addresses,
        'address_count': address_count,
        'secondary_address_count': secondary_address_count,
        'show_add_address_button': show_add_address_button,
    })

# View to update the quantity of a cart item
@require_POST  # Only allow POST requests
@login_required  # Ensures the user is logged in
def update_cart_item(request, item_id):
    # Get the cart item for the logged-in user or return 404
    item = get_object_or_404(CartItem, id=item_id, session__user=request.user)

    action = request.POST.get('action')  # Get the action (increase, decrease, or manual input)
    quantity = item.quantity  # Current quantity

    # Handle the different update actions
    if action == 'increase':
        quantity += 1
    elif action == 'decrease':
        quantity = max(1, quantity - 1)  # Prevent quantity from going below 1
    else:
        # Handle manual input of quantity
        try:
            quantity = int(request.POST.get('quantity', 1))
            quantity = max(1, quantity)
        except (ValueError, TypeError):
            quantity = 1  # Fallback to 1 on error

    # Save the updated quantity
    item.quantity = quantity
    item.save()
    
    # Redirect back to the cart view
    return redirect('cart:view_cart')

# View to remove a cart item
@require_POST  # Only allow POST requests
@login_required  # Ensures the user is logged in
def remove_cart_item(request, item_id):
    # Get the cart item for the logged-in user or return 404
    item = get_object_or_404(CartItem, id=item_id, session__user=request.user)
    item.delete()  # Delete the item from the cart
    return redirect('cart:view_cart')  # Redirect to cart view
