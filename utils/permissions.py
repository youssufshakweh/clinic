from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'patient')

class IsNutritionist(BasePermission): 
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'patient')