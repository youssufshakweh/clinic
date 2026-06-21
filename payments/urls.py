from django.urls import path
from . import views

urlpatterns = [
    path('cart/',                          views.CartView.as_view(),               name='cart'),
    path('cart/add/',                      views.AddToCartView.as_view(),          name='cart-add'),
    path('cart/<int:item_id>/update/',     views.UpdateCartItemView.as_view(),     name='cart-update'),
    path('cart/<int:item_id>/remove/',     views.RemoveCartItemView.as_view(),     name='cart-remove'),
    path('cart/checkout/',                 views.CheckoutView.as_view(),           name='cart-checkout'),
    path('orders/',                        views.OrderListView.as_view(),          name='order-list'),
    path('payments/submit/',               views.SubmitTransactionView.as_view(),  name='submit-transaction'),
]
