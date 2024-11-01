# cafe/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
# urls.py
#m
from .admin import admin_site  # import the custom admin site



urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    #m
    path('admin/', admin_site.urls),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_booking/', views.create_booking, name='create_booking'),  # Add this line for booking
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
