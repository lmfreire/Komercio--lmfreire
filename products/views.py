from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Product
from .serializers import ProductSerializer, DetailProductSerializer
from .permissions import IsAdminOrOwner, isSeller
from utils.mixins import MixinSerializer

class ProductView(MixinSerializer, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, isSeller]
    
    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductSerializer,
        "POST": DetailProductSerializer
    }
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class ProductDetailView(MixinSerializer, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]
    
    queryset = Product.objects.all()
    serializer_map = {
        "GET": DetailProductSerializer,
        "PATCH": DetailProductSerializer
    }