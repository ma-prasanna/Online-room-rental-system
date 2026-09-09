# mainapp/urls.py
from django.urls import path
from .views import home
from .views import user_login   # Import the view for the login page

urlpatterns = [
    path('home/', home, name='home'),
    path('userlogin/', user_login, name='user_login'),
    # Adjust the path as needed
    # Add other URL patterns as needed
]
