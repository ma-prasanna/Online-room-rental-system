from django.shortcuts import render
from mainapp.models import Room


# Create your views here.
def home(request):
    # Fetch all available rooms
    rooms = Room.objects.all()

    # Pass the rooms to the template

    return render(request, 'home.html', {'rooms': rooms})

def user_login(request):
    # Add logic for your login view
    return render(request, 'userlogin.html')