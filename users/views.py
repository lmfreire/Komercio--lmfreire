from rest_framework.views import APIView, Request, Response, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework import generics
from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserUpdateSerializer, SafeDeleteUserSerializer

from rest_framework.authentication import TokenAuthentication
from .permissions import IsOwner, IsAdm


class UserLoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(**serializer.validated_data)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key})
        
        return Response(
            {"detail": "invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    

class UserNewest(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    
    def get_queryset(self):
        max = self.kwargs['num']
        return self.queryset.order_by("-date_joined")[0:max]
    

class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    

class UserSafeDeleteView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]
    
    queryset = User.objects.all()
    serializer_class = SafeDeleteUserSerializer