from django.shortcuts import render


def display_events(request):
    return render(request, 'events.html')