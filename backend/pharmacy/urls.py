from django.urls import path
from .views import PharmacyListView, MedicineAvailabilityView, MedicineListView, StockViewSet, StockDetailView

urlpatterns = [
    path('list/', PharmacyListView.as_view(), name='pharmacy-list'),
    path('availability/', MedicineAvailabilityView.as_view(), name='medicine-availability'),
    path('medicines/', MedicineListView.as_view(), name='medicine-list'),
    path('stock/', StockViewSet.as_view(), name='stock-list'),
    path('stock/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
]
