from django.urls import path
from .views import PharmacyListView, MedicineAvailabilityView

urlpatterns = [
    path('list/', PharmacyListView.as_view(), name='pharmacy-list'),
    path('availability/', MedicineAvailabilityView.as_view(), name='medicine-availability'),
]
