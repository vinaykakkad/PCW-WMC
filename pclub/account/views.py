import os

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags
from django.contrib import messages
from django.db.models import Q

from .forms import LoginForm, RegisterForm
from .models import Account, AccountManager
from .utils import generate_token

# Create your views here.


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_PORT = os.getenv('EMAIL_PORT')
account_manager = AccountManager()


# Generating token and sending mail for activating account
def send_activation_email(request, user, email):
    current_site = get_current_site(request)
    subject = 'Brand Hunt-Activate your account'
    context = {'user': user, 'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': generate_token.make_token(user)}
    message = render_to_string('account/activate_link_generator.html', context)
    plain_message = strip_tags(message)

    send_mail(subject, plain_message, EMAIL_HOST_USER,
              [email], html_message=message)


class RegisterView(TemplateView):
    """
        Register View

        Renders registration page, verifies new user.
        On verification sends activation link.
    """

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        cf_username = request.POST.get('cf_username')
        fullname = request.POST.get('fullname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if cf_username == "":
            cf_username = None

        try:
            if cf_username is None:
                user = Account.objects.get(
                    Q(username=username) | Q(email=email))
            else:
                user = Account.objects.get(Q(username=username) | Q(
                    email=email) | Q(cf_username=cf_username))
        except Exception as identifier:
            user = None

        if user:
            messages.error(request, 'Username/Email already exists!!')
            return redirect('register')
        if not email.endswith('ahduni.edu.in'):
            messages.error(request, 'Only ahduni emails allowed!!')
            return redirect('register')
        if password1 != password2:
            messages.error(request, 'Passwords didn\'t match!!')
            return redirect('register')

        user = Account(username=username, email=email, cf_username=cf_username,
                       fullname=fullname, password=password1)
        user.set_password(password1)
        user.save()

        # Email verification is done by encoding user's primary key and generating a token
        send_activation_email(request, user, email)

        messages.info(
            request, 'Verification link sent. Check your email! Please wait for 5-7 minutes and check for SPAM/Promotions Folder in Gmail!')
        return redirect('user_login')


class LoginView(TemplateView):
    """
        Login View

        Renders login page and authenticates user.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        context = {'form': form}
        return render(request, 'account/login.html', context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
        except Exception as identifier:
            user = None

        if user:
            if not user.is_activated:
                messages.error(request, 'Account not activated.')
                return redirect('user_login')
            login(request, user)
            messages.info(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password.')
            return redirect('user_login')


class EmailActivateView(View):
    """
        Email Activation.

        Verification by decoding primary key and checking token
    """

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is None:
            messages.info(request, 'Verification failed!!')
        else:
            if generate_token.check_token(user, token):
                user.is_activated = True
                user.save()
                messages.info(request, 'Link verified successfully!!')
            else:
                messages.info(request, 'Verification failed!!')
        return redirect('user_login')


class ForgotPasswordView(View):
    """
        Forgot password view

        Getting email of the user and sending reset link.
    """

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'account/reset_email_getter.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email=email)
        except Exception as identifier:
            user = None

        if user is None:
            messages.error(request, 'Enter valid email address')
            return redirect('forgot_password')
        else:
            current_site = get_current_site(request)
            subject = 'Programming Club-Reset Password'

            context = {'user': user, 'domain': current_site.domain,
                       'encoded_username': urlsafe_base64_encode(force_bytes(user.username)),
                       'token': generate_token.make_token(user)}
            message = render_to_string(
                'account/reset_link_generator.html', context)
            plain_message = strip_tags(message)

            send_mail(subject, plain_message, EMAIL_HOST_USER,
                      [user.email], html_message=message)
            messages.info(request, 'Reset link sent, check your inbox.')
            return redirect('user_login')


class PasswordSetterView(View):
    """
        Resetting new password

        Getting new password and updating it.
    """

    def get(self, request, username64, token, *args, **kwargs):
        try:
            username = force_text(urlsafe_base64_decode(username64))
            user = Account.objects.get(username=username)
        except Exception as identifier:
            user = None

        if user is None:
            messages.error(request, 'Link verification failed!!')
            return redirect('forgot_password')
        else:
            if generate_token.check_token(user, token):
                context = {'username': user.username}
                return render(request, 'account/new_password.html', context)
            else:
                messages.info(request, 'Link verification failed!!')
                return redirect('forgot_password')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user = Account.objects.get(username=username)
            user.set_password(password1)
            user.save()
            messages.info(request, 'Password changed successfully!!')
            return redirect('user_login')
        else:
            messages.erroe(request, 'Passwords didn\'t match. Get link again.')
            return redirect('forgot_password')


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('user_login')
