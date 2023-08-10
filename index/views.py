from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .forms import SignUpForm


def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to your email {to_email} inbox and click on \
			received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')


def display_home(request):

    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']

        # Check if the provided username or email exists
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            # If the user is not found by username, try email
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            return redirect('login')
    else:
        return render(request, 'home.html')


@user_not_authenticated
def display_login(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


@user_not_authenticated
def display_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            user.save()

            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('home')

    else:
        form = SignUpForm()

    return render(
        request=request,
        template_name="sign_up.html",
        context={"form": form}
    )