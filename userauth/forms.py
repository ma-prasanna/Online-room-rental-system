# userauth/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OwnerProfile, TenantProfile
from .models import Room, Amenity, Message
from django.core.validators import RegexValidator

class OwnerSignupForm(UserCreationForm):
    phone_number = forms.CharField(
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')],
        max_length=10,
        min_length=10,
        help_text='Enter a valid 10-digit phone number.'
    )
    citizenship_photo = forms.ImageField()
    name = forms.CharField(max_length=100, help_text='Enter your name')
    email = forms.EmailField()  # Add this line to capture the email address

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone_number', 'password1', 'password2', 'citizenship_photo')
class TenantSignupForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    address = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    photo = forms.ImageField()

    class Meta:
        model = User
        fields = ['name', 'username', 'address', 'phone_number', 'photo', 'password1', 'password2']

    def save(self, commit=True):
        user = super(TenantSignupForm, self).save(commit=False)
        user.save()

        tenant_profile = TenantProfile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            address=self.cleaned_data['address'],
            phone_number=self.cleaned_data['phone_number'],
            photo=self.cleaned_data['photo'],
        )

        return user

#login ko lagi
class CustomAuthenticationForm(AuthenticationForm):
    user_type = forms.ChoiceField(choices=[('owner', 'Owner'), ('tenant', 'Tenant')])

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        if user_type not in ['owner', 'tenant']:
            raise forms.ValidationError("Invalid user type")
        return cleaned_data


#room ko formclass RoomForm(forms.ModelForm):
class RoomForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    latitude = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    longitude = forms.DecimalField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Room
        fields = ['title', 'no_of_room', 'no_of_bathroom', 'no_of_hall', 'location', 'price', 'amenities', 'room_photo', 'hall_photo', 'kitchen_photo', 'bathroom_photo', 'parking_area_photo', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        # Add additional styling or customization if needed


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'room']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['room'].required = False  # Ensure the room field is not required
