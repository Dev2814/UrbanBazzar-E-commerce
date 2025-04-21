from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.contrib import messages
from store.models import Product, ProductCategory, TryOnImage
from django.http import JsonResponse
from django.core.files.base import ContentFile
from io import BytesIO
import base64
from PIL import Image

# Create your views here.
def User_home(request):
    """Home view displaying featured products, categories, and recommendations"""
    # Fetch featured products with images
    featured_products = Product.objects.prefetch_related('images').order_by('?')

    # Fetch all categories with their related products and images
    categories = ProductCategory.objects.prefetch_related('product_set__images').all()

    # Fetch latest recommended products with images
    recommended_products = Product.objects.prefetch_related('images').order_by('?')

    context = {
        'products': featured_products,
        'categories': categories,
        'recommended_products': recommended_products,
    }
    return render(request, "urbanbazzar.html", context)

def About_us(request):
    return render(request, "Aboutus.html")

def Contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # You could log this or send an email here
        print(f"New Contact Message:\nName: {name}\nEmail: {email}\nMessage: {message}")
        
        messages.success(request, "Thanks for contacting us! We'll get back to you soon.")
        return redirect('Contact_us')
    
    return render(request, 'ContactUs.html')


def tryon_view(request):
    product_id = request.GET.get('xproduct_id')
    product = get_object_or_404(Product, id=product_id)

    tryon_image_qs = product.tryon_images.all()
    context = {'product': product}

    if tryon_image_qs.exists():
        tryon_image = tryon_image_qs.first()
        context['tag'] = tryon_image.tag
    else:
        context['tag'] = ''

    if request.method == 'POST':
        user_img = request.FILES.get('uploaded_image')

        if not tryon_image_qs.exists() or not user_img:
            context['error'] = 'Missing try-on image or uploaded image.'
            return render(request, 'Tryon.html', context)

        tryon_image = tryon_image_qs.first()

        api_url = ""
        # http://110.226.125.208:8888/v4/try_on
        payload = {
            'product_tag': tryon_image.tag,
        }
        files = {
            'user_img': user_img,
            'cloth_img': tryon_image.image.file,
        }
        try:
            response = requests.post(api_url, data=payload, files=files)
            if response.status_code == 200:
                message = response.json().get("message")
                result_url = response.json().get("data")
                image_url = result_url["image_preview_url"]
                
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    if image_response.status_code == 200:
                        image_data = image_response.content
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                        context['generated_base64'] = image_base64
                        print(image_base64)
                    else:
                        context['error'] = message
            else:
                context['error'] = message
        except Exception as e:
            context['error'] = f'Unexpected error: {e}'

    return render(request, 'Tryon.html', context)
