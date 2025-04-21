from django.apps import AppConfig
import threading


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    
    def ready(self):
        from .image_validator import process_product_images
        threading.Thread(target=process_product_images).start()
