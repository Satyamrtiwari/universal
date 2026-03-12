from django.urls import path
from .views import RegistrationView, LoginView, ProfileUpdateView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
]
