from django.contrib import admin
from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static

app = 'users'

urlpatterns = [
    path('login/user/', views.login_user, name = 'Login_user'),
    path('signup/user/', views.signup_user, name = 'Signup_user'),
    path('user/otp/', views.Verify_Login_otp, name = "Login_otp"),
    path('user/resendotp/', views.Resend_user_Login_otp, name = "Resend_otp"),
    path('user/forgetpassword/', views.password_reset_request, name = "send_password_reset_email"),
    path('user/forgetpassword/<int:user_id>/', views.Reset_password, name="Reset_password"),
    path('add-primary-address/', views.add_primary_address, name='add_primary_address'),
    path('add-secondary-address/', views.add_secondary_address, name='add_secondary_address'),
    path('logout/user/', views.logout_user, name='logout_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
