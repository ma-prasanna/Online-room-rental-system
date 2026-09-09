
from django.db import models

class Room(models.Model):
    AMENITIES_CHOICES = [
        ('wifi', 'Wi-Fi'),
        ('parking', 'Parking'),
        ('kitchen', 'Kitchen'),
        ('ac', 'Air Conditioning'),
        ('pet', 'Animal')
        # Add more amenities as needed
    ]

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/images', default=0)  # Assumes you have a 'room_images' folder in your media directory
    amenities = models.CharField(max_length=20, choices=AMENITIES_CHOICES)

    def __str__(self):
        return self.title
