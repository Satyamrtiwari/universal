from rest_framework import serializers
from .models import ConsultationRequest, Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class ConsultationRequestSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(read_only=True)
    
    class Meta:
        model = ConsultationRequest
        fields = '__all__'
        read_only_fields = ('patient', 'status', 'doctor', 'room_name')
