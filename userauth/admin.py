from django.contrib import admin
from .models import OwnerProfile, TenantProfile, Amenity, Room
from .models import User

# Register your models here.
admin.site.register(OwnerProfile)
admin.site.register(TenantProfile)
admin.site.register(Amenity)
admin.site.register(Room)
