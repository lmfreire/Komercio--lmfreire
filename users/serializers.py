from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from users.models import User

# from products.serializers import ProductSerializer

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "is_seller", "date_joined", "is_active", "is_superuser"]
        read_only_fields = ["is_active"]
        extra_kwargs = {
            "username": {'required': True},
            "first_name": {'required': True},
            "last_name": {'required': True},
            "is_seller": {'required': True},
            "password": {'write_only': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username']
            )
        ]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","first_name", "last_name", "is_seller", "date_joined", "is_active", "is_superuser"]
        read_only_fields = ["is_active"]
     
        
class SafeDeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","first_name", "last_name", "is_seller", "date_joined", "is_active"]
        read_only_fields = ["id","username","first_name", "last_name", "is_seller", "date_joined"]
        extra_kwargs = {
            "is_active": {'required': True},
        }
    