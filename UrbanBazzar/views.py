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

    # Prepare context dictionary to send to template
    context = {
        'products': featured_products,
        'categories': categories,
        'recommended_products': recommended_products,
    }
    return render(request, "urbanbazzar.html", context)

def About_us(request):
    # Renders the About Us page
    return render(request, "Aboutus.html")

def Contact_us(request):
    if request.method == 'POST':
        # Extract form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # You could log this or send an email here
        print(f"New Contact Message:\nName: {name}\nEmail: {email}\nMessage: {message}")
        
        # Show success message and redirect to Contact Us page
        messages.success(request, "Thanks for contacting us! We'll get back to you soon.")
        return redirect('Contact_us')
    
    # Render the Contact Us form template
    return render(request, 'ContactUs.html')


def tryon_view(request):
    # Get product_id from GET parameters
    product_id = request.GET.get('xproduct_id')
    product = get_object_or_404(Product, id=product_id)

    # Get related try-on image(s)
    tryon_image_qs = product.tryon_images.all()
    context = {'product': product}

    if tryon_image_qs.exists():
        # Use the first try-on image's tag
        tryon_image = tryon_image_qs.first()
        context['tag'] = tryon_image.tag
    else:
        # Set empty tag if no try-on image
        context['tag'] = ''

    if request.method == 'POST':
        # Get uploaded image from form
        user_img = request.FILES.get('uploaded_image')

        # If try-on image or user image is missing, return error
        if not tryon_image_qs.exists() or not user_img:
            context['error'] = 'Missing try-on image or uploaded image.'
            return render(request, 'Tryon.html', context)

        tryon_image = tryon_image_qs.first()

        api_url = "#"
        
        payload = {
            'product_tag': tryon_image.tag,
        }
        files = {
            'user_img': user_img,
            'cloth_img': tryon_image.image.file,
        }
        try:
            # Send POST request to try-on API
            response = requests.post(api_url, data=payload, files=files)
            if response.status_code == 200:
                # Parse API response
                message = response.json().get("message")
                result_url = response.json().get("data")
                image_url = result_url["image_preview_url"]
                
                # Get the generated image from URL
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    if image_response.status_code == 200:
                        image_data = image_response.content
                        # Convert image to base64
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                        context['generated_base64'] = image_base64
                    else:
                        # Set error if image fetch failed
                        context['error'] = message
            else:
                # Set error from API response
                context['error'] = message
        except Exception as e:
            # Handle unexpected errors
            context['error'] = f'Unexpected error: {e}'

    # Render Tryon page with context
    return render(request, 'Tryon.html', context)
