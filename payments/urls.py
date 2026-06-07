from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.CartView.as_view(),           name='cart'),
    path('add/',                      views.AddToCartView.as_view(),      name='cart-add'),
    path('<int:item_id>/update/',     views.UpdateCartItemView.as_view(), name='cart-update'),
    path('<int:item_id>/remove/',     views.RemoveCartItemView.as_view(), name='cart-remove'),
    path('checkout/',                 views.CheckoutView.as_view(),       name='cart-checkout'),
]
