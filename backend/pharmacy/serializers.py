from rest_framework import serializers
from .models import Pharmacy, Medicine, Stock

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    medicine_name = serializers.ReadOnlyField(source='medicine.name')
    pharmacy_name = serializers.ReadOnlyField(source='pharmacy.name')
    
    class Meta:
        model = Stock
        fields = '__all__'
