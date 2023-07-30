from django.shortcuts import render


def display_landing(request):
    return render(request, 'landing.html')