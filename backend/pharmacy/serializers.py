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
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), source='medicine'
    )
    
    class Meta:
        model = Stock
        fields = ('id', 'medicine_id', 'medicine_name', 'pharmacy_name', 'quantity', 'is_available')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        # Only show quantity to Pharmacists
        if request and request.user.is_authenticated:
            if request.user.role != 'PHARMACIST':
                representation.pop('quantity', None)
        else:
            # Hide for anonymous users as well
            representation.pop('quantity', None)
        return representation
