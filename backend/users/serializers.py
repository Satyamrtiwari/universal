from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=False, default='PATIENT')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'role', 'phone_number', 'area_village', 'pincode')
    
    def create(self, validated_data):
        # Default role to PATIENT if not provided (for app side)
        role = validated_data.get('role', 'PATIENT')
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=role,
            phone_number=validated_data.get('phone_number', ''),
            area_village=validated_data.get('area_village', ''),
            pincode=validated_data.get('pincode', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
