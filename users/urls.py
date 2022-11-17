from django.urls import path
from . import views 

urlpatterns = [
    path('accounts/', views.UserView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('accounts/newest/<int:num>/', views.UserNewest.as_view()),
    path('accounts/<pk>/', views.UserUpdateView.as_view()),
    path('accounts/<pk>/management/', views.UserSafeDeleteView.as_view()),
]
