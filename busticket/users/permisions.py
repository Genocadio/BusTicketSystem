from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'admin'
    
class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'normal'