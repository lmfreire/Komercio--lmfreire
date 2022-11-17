from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser

class isSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        
        return request.method in SAFE_METHODS or request.user.is_seller
       