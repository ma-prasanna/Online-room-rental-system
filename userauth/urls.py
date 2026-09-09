# userauth/urls.py
from django.urls import path, reverse_lazy
from .views import owner_signup, tenant_signup, tenant_dashboard, send_message, room_messages
from .views import custom_login, owner_dashboard, add_room, delete_room, room_detail
from django.conf.urls.static import static
from django.conf import settings
from .views import available_rooms, room_detail_available, choose_user_type
from .views import custom_logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('owner_signup/', owner_signup, name='owner_signup'),
    path('tenant_signup/', tenant_signup, name='tenant_signup'),
    path('user/', choose_user_type, name='choose_user_type'),
    path('login/', custom_login, name='login'),
    path('owner_dashboard/', owner_dashboard, name='owner_dashboard'),
    path('tenant_dashboard/', tenant_dashboard, name='tenant_dashboard'),
    path('add_room/', add_room, name='add_room'),
    path('delete_room/<int:room_id>/', delete_room, name='delete_room'),
    path('room_detail/<int:room_id>/', room_detail, name='room_detail'),
    path('', available_rooms, name='available_rooms'),
    path('room/<int:room_id>/', room_detail_available, name='room_detail_available'),
    path('logout/', custom_logout, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('send_message/<int:room_id>/', send_message, name='send_message'),
    path('room_messages/<int:room_id>/', room_messages, name='room_messages'),

    # Add other authentication-related URL patterns as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)