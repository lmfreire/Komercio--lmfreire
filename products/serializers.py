from rest_framework import serializers

from users.serializers import UserRegisterSerializer

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["user"]
        
    
class DetailProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
    user = UserRegisterSerializer(read_only=True)
