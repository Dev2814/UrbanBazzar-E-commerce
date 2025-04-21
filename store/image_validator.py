import os
import requests
from urllib.request import urlopen
from django.core.files.base import ContentFile
from .models import Product, TryOnImage

API_URL = ""  # Add the correct API URL

def process_product_images():
    print("🔄 Starting product image validation...")

    all_products = Product.objects.all()

    for product in all_products:
        product_urls = []  # To collect image URLs for each product

        for product_img in product.images.all():
            original_file_name = os.path.basename(product_img.image.name)

            if product.tryon_images.filter(image__endswith=original_file_name).exists():
                print(f"🟡 Product '{product.name}' already has a validated image: {original_file_name}")
                break
        else:
            for product_img in product.images.all():
                try:
                    img_path = product_img.image.path
                    original_file_name = os.path.basename(product_img.image.name)

                    with open(img_path, 'rb') as img_file:
                        response = requests.post(
                            API_URL,
                            files={"image": img_file},
                            data={"product_id": product.id}
                        )
                        if response.status_code == 200:
                            data = response.json()
                            image_url = data.get("image_url")
                            tag = data.get("tag", "")

                            if image_url:
                                resp = urlopen(image_url)
                                img_data = resp.read()
                                file_name = os.path.basename(image_url)

                                # Save the Try-On Image
                                tryon_image = TryOnImage(
                                    product=product,
                                    tag=tag
                                )
                                tryon_image.image.save(file_name, ContentFile(img_data), save=True)

                                print(f"✅ Saved Try-On Image for '{product.name}' with tag '{tag}'")

                                # Add the image URL to the list for the product
                                product_urls.append(image_url)

                            else:
                                print("⚠️ No image_url returned from API")
                        else:
                            print(f"❌ API error for {original_file_name}: {response.status_code}")
                except Exception as e:
                    print(f"💥 Error processing image '{product_img.image.name}': {e}")

            # After processing all images, update the product's image URLs
            if product_urls:
                product.product_url = product_urls  # Assuming product_url is a list of URLs
                product.save()
                print(f"✅ Updated product '{product.name}' with {len(product_urls)} image URLs.")
    
    print("✅ Image validation completed.")








