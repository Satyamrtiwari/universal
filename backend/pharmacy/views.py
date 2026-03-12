from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Pharmacy, Medicine, Stock
from .serializers import PharmacySerializer, StockSerializer

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
