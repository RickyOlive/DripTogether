from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def display_landing(request):

    if User.is_authenticated:
        print(request.user.username)

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
            return redirect('landing')
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            return redirect('login')
    else:
        return render(request, 'landing.html')


def display_login(request):
    return render(request, 'login.html')