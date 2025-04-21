from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UserAddress
from .forms import UserAddressForm, UserSecondaryAddressForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import pyotp
import io as io_module
import qrcode
from io import BytesIO
import io as io_module
from django.utils.html import strip_tags


# Get the user model
User = get_user_model()

def send_signup_email(request, email, firstname):
    """Sends a signup confirmation email to the user."""
    subject = "🎉 Welcome to UrbanBazzar! Your Signup is Successful"
    from_email = "UrbanBazzar Support <support@urbanbazzar.com>"
    to_email = [email]

    # Context for rendering the email template
    context = {
        'firstname': firstname,
        'support_email': 'support@urbanbazzar.com',
        'help_center_url': 'http://localhost:2814/contact',  # Update when live
    }

    # Render email content
    message = render_to_string('emails/signup_email.html', context)

    # Send email
    email_message = EmailMultiAlternatives(subject, message, from_email, to_email)
    email_message.content_subtype = "html"
    email_message.send()

def sending_login_otp_email(user_email, otp_secret):
    """Creates a QR code and sends the OTP email using the provided OTP secret."""

    # Generate OTP Auth URL using the provided secret
    otp_auth_url = pyotp.totp.TOTP(otp_secret).provisioning_uri(user_email, issuer_name="UrbanBazzar")

    # Generate QR Code
    qr = qrcode.make(otp_auth_url)
    qr_io = io_module.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)

    # Render email template
    html_content = render_to_string("emails/otp_email.html", {"user_email": user_email})

    # Send email
    subject = "UrbanBazzar Login OTP"
    email = EmailMultiAlternatives(
        subject,
        strip_tags(html_content),
        'UrbanBazzar Security <support@urbanbazzar.com>',
        [user_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.attach("otp_qr.png", qr_io.getvalue(), "image/png")
    email.send()

def sending_resended_otp_email(user_email, otp_secret):
    """Sends a resent OTP email with a QR code."""
    
    # Generate OTP Auth URL
    otp_auth_url = pyotp.totp.TOTP(otp_secret).provisioning_uri(user_email, issuer_name="UrbanBazzar")
    
    # Generate QR Code
    qr = qrcode.make(otp_auth_url)
    qr_io = io_module.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    
    # Render email template
    html_content = render_to_string("emails/resend_otp_email.html", {"user_email": user_email})
    
    # Send email
    subject = "UrbanBazzar Resent OTP"
    email = EmailMultiAlternatives(
        subject,
        strip_tags(html_content),
        'UrbanBazzar Security <support@urbanbazzar.com>',
        [user_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.attach("otp_qr.png", qr_io.getvalue(), "image/png")
    email.send()

def send_Login_email(request, email, firstname):
    """Sends a Login confirmation email to the user."""
    subject = "🎉 Welcome to UrbanBazzar! Your Login In UrbanBazzar is Successful"
    from_email = "UrbanBazzar Support <support@urbanbazzar.com>"
    to_email = [email]

    # Context for rendering the email template
    context = {
        'firstname': firstname,
        'support_email': 'support@urbanbazzar.com', #update when live with own domain
        'help_center_url': 'http://localhost:2814/contact',  # Update when live
    }

    # Render email content
    message = render_to_string('emails/Login_email.html', context)

    # Send email
    email_message = EmailMultiAlternatives(subject, message, from_email, to_email)
    email_message.content_subtype = "html"
    email_message.send()

def Deactivate_account_sending_email(email):
    """Sends an email warning about account deactivation due to multiple failed OTP attempts."""
    context = {'support_email': 'support@urbanbazzar.com'}
    html_content = render_to_string("emails/account_deactivation_warning.html", context)

    email_message = EmailMultiAlternatives(
        "UrbanBazzar Account Warning",
        strip_tags(html_content),
        "UrbanBazzar Security <support@urbanbazzar.com>",
        [email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

def send_password_reset_email(user, reset_link):
    """Sends a password reset email using an HTML template."""
    subject = "🔐 UrbanBazzar: Reset Your Password"
    from_email = "UrbanBazzar Support <support@urbanbazzar.com>"
    to_email = [user.email]

    # Render the email template from 'emails/password_reset_email.html'
    message = render_to_string("emails/password_reset_email.html", {"user": user, "reset_link": reset_link})

    mail = EmailMultiAlternatives(subject, message, from_email, to_email)
    mail.content_subtype = "html"  # Set email content as HTML
    mail.send()

def send_successful_reset_password_mail(user):
    """Sends an email notifying the user that their password has been successfully changed."""
    subject = " UrbanBazzar: Password Successfully Changed"
    from_email = "UrbanBazzar Support <support@urbanbazzar.com>"
    to_email = [user.email]
    login_url = "http://127.0.0.1:2814/login/user/"
    
    # Render the email content from a template
    html_message = render_to_string("emails/successful_password_reset.html", {"user": user, "login_url": login_url })
    plain_message = strip_tags(html_message)
    
    mail = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
    mail.attach_alternative(html_message, "text/html")
    mail.send()


def signup_user(request):
    """Handles user signup, validates input, and sends a confirmation email."""
    if request.method == "POST":
        fullname = request.POST.get("fullname", "").strip()
        first_name, last_name = (fullname.split(" ", 1) + [""])[:2]
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirmpassword", "").strip()

        # Server-side validation
        if not fullname:
            messages.error(request, "Full Name is required.")
        elif not username:
            messages.error(request, "Username is required.")
        elif not email:
            messages.error(request, "Email is required.")
        elif not password:
            messages.error(request, "Password is required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
        else:
            # Create an inactive user
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password,
            )
            user.first_name = first_name
            user.last_name = last_name
            user.role = role
            user.save()

            # Store in session
            request.session['first_name'] = first_name

            # Send signup confirmation email
            send_signup_email(request, email, first_name)

            messages.success(
                request, "Signup successful! A verification link has been sent to your email."
            )
            return redirect("users:Login_user")
    
    return render(request, "users/Signup_user.html")

def login_user(request):
    """Handles user login with email and password authentication."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email:
            messages.error(request, "Email ID is required")
            return redirect('users:Login_user')

        if not password:
            messages.error(request, "Password is required")
            return redirect('users:Login_user')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Scan The QR Code in your Email and Enter The OTP to Log In to UrbanBazzar")

            otp_secret = request.session.get('otp_secret', pyotp.random_base32())
            request.session['otp_secret'] = otp_secret
            request.session['email'] = user.email
            request.session['user_name'] = user.username

            # Send OTP via email
            sending_login_otp_email(user.email, otp_secret)

            return redirect("users:Login_otp")
        else:
            messages.error(request, "Invalid email or password")
            return redirect('users:Login_user')   
    
    return render(request, "users/Login_user.html")

def Verify_Login_otp(request):
    """Verifies the OTP entered by the user and locks the account after 3 failed attempts."""
    if request.method == "POST":
        Full_Otp = "".join(filter(str.isdigit, ''.join(request.POST.get(f'otp{i}', "").strip() for i in range(1, 7))))
        otp_secret = request.session.get('otp_secret')
        email = request.session.get('email')
        first_name = request.session.get('first_name')

        if not otp_secret or not email:
            messages.error(request, "Session expired. Please log in again.")
            return redirect('users:Login_user')

        # Track OTP attempts
        attempt_count = request.session.get('otp_attempts', 0)

        user = User.objects.get(email=email)

        if pyotp.TOTP(otp_secret).verify(Full_Otp, valid_window=1):
            login(request, user)
            request.session['otp_attempts'] = 0  # Reset attempts on success
            messages.success(request, "OTP Verified! You are logged in now!")
            # Sending Successfull Login Email 
            send_Login_email(request, email, first_name)
            return redirect('home')
        
        else:
            attempt_count += 1
            request.session['otp_attempts'] = attempt_count

            if attempt_count >= 3:

                user.is_active = False
                user.save()

                Deactivate_account_sending_email(email)
                messages.error(request, "Too many failed OTP attempts! Contact the admin.")
                return redirect('users:Login_user')
            
            messages.error(request, "Invalid OTP! Please try again.")
            return redirect('users:Login_otp')
    
    return render(request, 'users/Login_otp.html')

def Resend_user_Login_otp(request):
    """Handles OTP resend request and sends a new OTP to the user."""
    email = request.session.get('email')
    
    if not email:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('users:Login_user')
    
    user = User.objects.filter(email=email).first()
    if not user:
        messages.error(request, "User not found. Please log in again.")
        return redirect('users:Login_user')
    
    # Generate a new OTP secret
    otp_secret = pyotp.random_base32()
    request.session['otp_secret'] = otp_secret
    
    # Send the new OTP via email
    sending_resended_otp_email(user.email, otp_secret)
    
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('users:Login_otp')

def password_reset_request(request):
    """Handles password reset requests and sends a reset link to the user's email."""
    if request.method == "POST":
        email = request.POST.get("email")

        # Check if the email exists in the database
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("User Exists with Email!!")

            # Generate the password reset link
            reset_link = f"http://127.0.0.1:2814/user/forgetpassword/{user.id}/"

            # Send the password reset email with reset_link
            send_password_reset_email(user, reset_link)

            messages.success(request, "Password reset link sent to your email.")
        else:
            messages.error(request, "User does not exist!!")

    return render(request, 'users/Forgetpassword.html')

def Reset_password(request, user_id):  
    """Handles password reset by updating the user's password."""
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        if not password or not confirmpassword:
            messages.error(request, "All fields are required.")
            return redirect("Reset_password", user_id=user.id)

        # Validate if password and confirm password match
        if password != confirmpassword:
            messages.error(request, "Password does not match the Confirm Password")
            return redirect("Reset_password", user_id=user.id)
        else:
            # Update the user's password
            user.set_password(password)
            user.save()
            
            # Send success email notification
            send_successful_reset_password_mail(user)
            
            messages.success(request, "New password has been updated successfully")
            login(request, user)
            return redirect("users:Login_user")
    
    return render(request, "users/Resetpassword.html", {"user": user})


# View to add a primary address
@login_required
def add_primary_address(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            primary_address = form.save(commit=False)
            primary_address.user = request.user
            primary_address.save()
            messages.success(request, "Primary address saved successfully.")
            return redirect('cart:view_cart')  # Redirect to the cart view after saving
    else:
        form = UserAddressForm()
    return render(request, 'users/add_address_modal.html', {'form': form})

# View to add a secondary address
@login_required
def add_secondary_address(request):
    if request.method == 'POST':
        form = UserSecondaryAddressForm(request.POST)
        if form.is_valid():
            secondary_address = form.save(commit=False)
            secondary_address.user = request.user
            secondary_address.save()
            messages.success(request, "Secondary address saved successfully.")
            return redirect('cart:view_cart')  # Redirect to the cart view after saving
    else:
        form = UserSecondaryAddressForm()
    return render(request, 'users/add_address_modal.html', {'form': form})


def logout_user(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('users:Login_user')
