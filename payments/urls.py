from django.contrib import admin
from django.urls import path
from payments import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'payments'

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
