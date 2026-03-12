from django.urls import path
from .views import RegistrationView, LoginView, ProfileUpdateView, DoctorListView, PatientHealthHistoryView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('health-history/', PatientHealthHistoryView.as_view(), name='health-history'),
]
