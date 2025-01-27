from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['firs_name', 'last_name', 'mobile_number', 'email', 'password']
        extra_kwargs = {'passwword': {'write_only': True}}
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class LoginSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User  # مدل مربوطه (مثلاً User) را وارد کنید
        fields = ['mobile_number', 'password']
    
    def validate(self, data):
        user = authenticate(mobile_number=data['mobile_number'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid mobile number or password.")
        return user
    