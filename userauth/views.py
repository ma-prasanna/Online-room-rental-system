# userauth/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import OwnerSignupForm, TenantSignupForm, RoomForm, MessageForm
from .models import OwnerProfile, TenantProfile, Room, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def owner_signup(request):
    if request.method == 'POST':
        form = OwnerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            name = form.cleaned_data['name']  # Get the name from the form
            email = form.cleaned_data['email']
            # Check if the email is provided, otherwise use a default value
            if not email:
                email = 'dosroghar@email.com'

            owner_profile = OwnerProfile(user=user, citizenship_photo=form.cleaned_data['citizenship_photo'], phone_number=phone_number, name=name, email=email)
            owner_profile.save()



            # Send email to admin using the email address provided during signup
            send_owner_signup_notification(user.email)

            # Show success message
            messages.success(request, 'Account created successfully. Please Login <i class="fa-regular fa-face-smile"></i>')

            # Redirect to a success page or login page
            return redirect('login')
    else:
        form = OwnerSignupForm()

    return render(request, 'owner_signup.html', {'form': form})

def send_owner_signup_notification(owner_email):
    # This function sends an email to the admin when a new owner signs up
    subject = 'New Owner Signup'
    message = f'A new owner has signed up.\nEmail: {owner_email}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['mallaprasanna18@gmail.com']
    send_mail(subject, message, from_email, recipient_list)

def tenant_signup(request):
    if request.method == 'POST':
        form = TenantSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Check if a TenantProfile already exists for the user
            tenant_profile, created = TenantProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': form.cleaned_data['name'],
                    'address': form.cleaned_data['address'],
                    'phone_number': form.cleaned_data['phone_number'],
                    'photo': form.cleaned_data['photo'],
                }
            )

            if not created:
                # Update the existing TenantProfile if it already exists
                tenant_profile.name = form.cleaned_data['name']
                tenant_profile.address = form.cleaned_data['address']
                tenant_profile.phone_number = form.cleaned_data['phone_number']
                tenant_profile.photo = form.cleaned_data['photo']
                tenant_profile.save()

            # Show success message
            messages.success(request, 'Account created successfully. Please Login <i class="fa-regular fa-face-smile"></i>')

            # Redirect to the tenant dashboard
            return redirect('login')
    else:
        form = TenantSignupForm()

    return render(request, 'tenant_signup.html', {'form': form})


#login ko lagi
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user_type == 'owner':
                    return redirect('owner_dashboard')  # Redirect to owner dashboard
                elif user_type == 'tenant':
                    return redirect('tenant_dashboard')  # Redirect to tenant dashboard or home

    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})



#dashboar ko lagi
@login_required(login_url='login')
def owner_dashboard(request):
    # Retrieve rooms belonging to the logged-in owner
    rooms = Room.objects.filter(owner=request.user)

    # Retrieve owner profile information
    owner_profile = OwnerProfile.objects.get(user=request.user)

    return render(request, 'owner_dashboard.html', {'rooms': rooms, 'owner_profile': owner_profile})

@login_required
def tenant_dashboard(request):
    tenant_profile = TenantProfile.objects.get(user=request.user)
    return render(request, 'tenant_dashboard.html', {'tenant_profile': tenant_profile})


@login_required
def dashboard(request):
    if request.user.is_owner:
        owner_profile = OwnerProfile.objects.get(user=request.user)
        return render(request, 'owner_dashboard.html', {'owner_profile': owner_profile})
    elif request.user.is_tenant:
        tenant_profile = TenantProfile.objects.get(user=request.user)
        return render(request, 'tenant_dashboard.html', {'tenant_profile': tenant_profile})
    else:
        # Handle cases where the user has no profile or an unknown user type
        return render(request, 'unknown_user_type.html')

@login_required(login_url='login')
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            form.save_m2m() # Save the many-to-many relationships
            return redirect('owner_dashboard')
    else:
        form = RoomForm()

    return render(request, 'add_room.html', {'form': form})

@login_required(login_url='login')
def delete_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        if room.owner == request.user:
            room.delete()
            return redirect('owner_dashboard')

    return render(request, 'delete_room_confirm.html', {'room': room})

@login_required(login_url='login')
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    amenities = room.amenities.all()  # Fetch all amenities related to the room
    return render(request, 'room_detail.html', {'room': room, 'amenities': amenities})




def available_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'available_rooms.html', {'rooms': rooms})



def room_detail_available(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Get the user who uploaded the room
    room_owner = room.owner

    try:
        # Retrieve the OwnerProfile for the room owner
        owner_profile = OwnerProfile.objects.get(user=room_owner)
    except OwnerProfile.DoesNotExist:
        # Handle the case where no OwnerProfile is found for the room owner
        owner_profile = None  # Set to a default value or handle accordingly

    amenities = room.amenities.all()  # Fetch all amenities related to the room

    return render(request, 'room_detail_available.html',
                  {'owner_profile': owner_profile, 'room': room, 'amenities': amenities})

def choose_user_type(request):
    return render(request, 'choose_user_type.html')


def custom_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the name of your login URL or the actual URL


def about(request):
    # your view logic here
    return render(request, 'about.html')



def send_message(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    owner_profile = room.owner.ownerprofile

    if request.method == 'POST':
        form = MessageForm(request.POST, initial={'room': room})
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.receiver = room.owner  # Set the receiver field
            message.save()


            messages.success(request, 'Your message has been sent successfully!')
            return redirect('room_detail_available', room_id=room_id)
    else:
        form = MessageForm(initial={'room': room})

    context = {
        'room': room,
        'owner_profile': owner_profile,
        'amenities': room.amenities.all(),
        'form': form,
    }

    if request.user.is_authenticated:
        return render(request, 'room_detail_available.html', context)
    else:
        return render(request, 'room_detail_available.html', context)


def room_messages(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room)

    return render(request, 'room_messages.html', {'room': room, 'messages': messages})


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x.price < pivot.price]
    middle = [x for x in arr if x.price == pivot.price]
    right = [x for x in arr if x.price > pivot.price]
    return quicksort(left) + middle + quicksort(right)
def available_rooms(request):
    if request.method == 'GET' and 'location' in request.GET:
        location_query = request.GET.get('location')
        rooms = Room.objects.filter(location__icontains=location_query)

    else:
        rooms = Room.objects.all()

    # Use quicksort to manually sort the list of rooms by price
    sorted_rooms = quicksort(list(rooms))

    context = {
        'rooms': sorted_rooms,
    }

    return render(request, 'available_rooms.html', context)