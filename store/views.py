from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductImage
from django.db.models import Q 
from django.core.paginator import Paginator
from orders.models import OrderDetails, OrderItems
from users.models import UserAddress, UserPayment, UserSecondaryAddress
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import ProductForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# View for displaying detailed product page
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Find related products with same brand or category
    related_products = Product.objects.filter(
        Q(brand_name=product.brand_name) | Q(product_category=product.product_category)
    ).exclude(id=product.id)[:48]

    # Chunk related products into sets of 3 for carousel
    related_chunks = [related_products[i:i + 3] for i in range(0, len(related_products), 3)]

    context = {
        'product': product,
        'related_products': related_products,
        'related_chunks': related_chunks,
    }
    return render(request, 'store/product_detail.html', context)

# View for listing products with optional search
def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        try:
            float(query)
            price_filter = Q(price__exact=query)
        except ValueError:
            price_filter = Q()

        # Filter by name, description, brand or exact price
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(brand_name__icontains=query) |
            price_filter
        ).distinct()

    products = products.order_by('-id')  # Show newest first

    paginator = Paginator(products, 15)  # Paginate with 15 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/products.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'query': query,
    })

# View for vendor dashboard
@login_required
def vender_dashboard(request):
    vendor = request.user

    # Restrict access to vendors only
    if not vendor.role == 'vendor':
        return redirect('store:product_list')

    # Get vendor-specific data
    products = Product.objects.filter(vendor=vendor)
    vendor_orders = OrderDetails.objects.filter(
        orderitems__product__vendor=vendor
    ).distinct()

    total_sales = OrderItems.objects.filter(
        product__vendor=vendor,
        order__status='completed'
    ).aggregate(total=Sum('product__price'))['total'] or 0

    total_products_sold = OrderItems.objects.filter(
        product__vendor=vendor
    ).aggregate(total=Sum('quantity'))['total'] or 0

    pending_payments = vendor_orders.filter(
        status='completed',
        payment__isnull=True
    ).count()

    # Optional user info
    user_address = UserAddress.objects.filter(user=vendor).first()
    user_secondary_address = UserSecondaryAddress.objects.filter(user=vendor).first()
    user_payment = UserPayment.objects.filter(user=vendor).first()

    context = {
        'vendor': vendor,
        'products': products,
        'orders': vendor_orders,
        'total_sales': total_sales,
        'total_products_sold': total_products_sold,
        'pending_payments': pending_payments,
        'user_address': user_address,
        'user_secondary_address': user_secondary_address,
        'user_payment': user_payment,
    }

    return render(request, 'store/Vender_dashboard.html', context)

# View for adding a new product
@login_required
def add_product(request):
    ImageFormSet = modelformset_factory(ProductImage, fields=('image',), extra=3, can_delete=True)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()

            # Save uploaded images
            for image_form in formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()

            messages.success(request, "Product added successfully!")
            return redirect('store:vender_dashboard')
    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())

    return render(request, 'store/add_product.html', {
        'form': form,
        'formset': formset,
    })

# View for editing a product
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('store:vender_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

# View for deleting a product
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('store:vender_dashboard')

# View for updating order status
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(OrderDetails, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in dict(OrderDetails.STATUS_CHOICES):
            # If cancelled, restore stock
            if new_status == 'cancelled' and order.status != 'cancelled':
                for item in order.orderitems.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()

            # Update status
            order.status = new_status
            order.save()

            messages.success(request, 'Order status updated.')

        return redirect('store:vender_dashboard')

    return render(request, 'store/update_order_status.html', {'order': order})
