from django.db import models
from users.models import CustomUser  
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True, limit_choices_to={'role': 'vendor'})  # Link Vendor
    stock = models.PositiveIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"
    

class TryOnImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tryon_images")
    image = models.ImageField(upload_to="tryon_images/")
    tag = models.CharField(max_length=100, blank=True, help_text="e.g. front view, side view")

    def __str__(self):
        return f"Try-On Image for {self.product.name}"
    
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         # Open the uploaded image
    #         img = Image.open(self.image)

    #         # Convert to RGB if needed
    #         if img.mode in ("RGBA", "P"):
    #             img = img.convert("RGB")

    #         # Resize logic
    #         width, height = img.size
    #         if width == height:
    #             new_size = (640, 640)
    #         else:
    #             ratio = height / width
    #             new_size = (640, int(640 * ratio))

    #         img = img.resize(new_size, Image.Resampling.LANCZOS)

    #         # Save resized image to memory
    #         buffer = BytesIO()
    #         img.save(buffer, format='JPEG', quality=90)
    #         buffer.seek(0)

    #         # Replace original image with resized image
    #         file_name = os.path.basename(self.image.name)
    #         self.image = ContentFile(buffer.read(), name=file_name)

    #     # Now save as usual
    #     super().save(*args, **kwargs)
        

