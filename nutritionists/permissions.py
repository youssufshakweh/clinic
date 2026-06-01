from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsNutritionistOwnerOrReadOnly(BasePermission):
    """
    - أي شخص يقدر يشوف (GET)
    - التعديل/الحذف/الـ actions: الأخصائي صاحب المنتج بس
    """

    def has_permission(self, request, view):
        # أي شخص يشوف
        if request.method in SAFE_METHODS:
            return True
        # باقي العمليات: لازم يكون أخصائي
        return hasattr(request.user, 'nutritionist_profile')

    def has_object_permission(self, request, view, obj):
        # أي شخص يشوف
        if request.method in SAFE_METHODS:
            return True
        # التعديل: صاحب المنتج بس
        return obj.nutritionist == request.user.nutritionist_profile