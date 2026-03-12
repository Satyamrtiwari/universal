from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Pharmacy, Medicine, Stock
from .serializers import PharmacySerializer, StockSerializer,MedicineSerializer

class PharmacyListView(generics.GenericAPIView):
    serializer_class = PharmacySerializer
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        area = request.query_params.get('area', None)
        if area:
            queryset = Pharmacy.objects.filter(area_village__icontains=area)
        else:
            queryset = Pharmacy.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MedicineAvailabilityView(generics.GenericAPIView):
    serializer_class = StockSerializer
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        medicine_name = request.query_params.get('medicine', None)
        area = request.query_params.get('area', None)
        
        queryset = Stock.objects.filter(is_available=True)
        
        if medicine_name:
            queryset = queryset.filter(medicine__name__icontains=medicine_name)
        if area:
            queryset = queryset.filter(pharmacy__area_village__icontains=area)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

class StockViewSet(generics.ListCreateAPIView):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PHARMACIST':
            # Filter stock by the pharmacy owned by the logged-in user
            return Stock.objects.filter(pharmacy__owner=user)
        return Stock.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'pharmacy'):
            serializer.save(pharmacy=user.pharmacy)
        else:
            # Fallback or create a pharmacy for the user
            pharmacy, created = Pharmacy.objects.get_or_create(
                owner=user,
                defaults={'name': user.store_name or f"{user.username}'s Pharmacy", 'area_village': user.area_village or "Nabha"}
            )
            serializer.save(pharmacy=pharmacy)

class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]
