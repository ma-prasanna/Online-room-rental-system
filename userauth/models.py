from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

class OwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    citizenship_photo = models.ImageField(upload_to='citizenship_photos/')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='tenant_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


#room adding

class Amenity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Room(models.Model):
    title = models.CharField(max_length=100)
    no_of_room = models.IntegerField()
    no_of_bathroom = models.IntegerField()
    no_of_hall = models.IntegerField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField(Amenity)

    room_photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    hall_photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    kitchen_photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    bathroom_photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    parking_area_photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    description = models.TextField(blank=True, null=True)

    # Additional fields as per your requirements

    def __str__(self):
        return self.title



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} - {self.timestamp}"
