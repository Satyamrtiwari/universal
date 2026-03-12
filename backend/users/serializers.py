from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Simplified registration: Username and Password only (Email optional).
    Role defaults to PATIENT for the app.
    """
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=False, default='PATIENT')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'role')
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'PATIENT')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating the profile AFTER login.
    """
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'age', 'phone_number', 'address', 'area_village', 'pincode')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
