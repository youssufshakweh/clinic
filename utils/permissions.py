from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'patient')

class IsNutritionist(BasePermission): 
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'patient')


class IsPatientUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'patient_profile')
        )


class IsNutritionistUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'nutritionist_profile')
        )