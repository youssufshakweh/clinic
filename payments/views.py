from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
)
from utils.permissions import IsPatientUser


class CartView(APIView):
    permission_classes = [IsPatientUser]

    def get(self, request):
        patient = request.user.patient_profile
        cart, _ = Cart.objects.get_or_create(patient=patient)
        return Response(CartSerializer(cart).data)


class AddToCartView(APIView):
    permission_classes = [IsPatientUser]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        patient = request.user.patient_profile
        cart, _ = Cart.objects.get_or_create(patient=patient)

        product = serializer.validated_data.get('product')
        package = serializer.validated_data.get('package')
        quantity = serializer.validated_data.get('quantity', 1)

        if product:
            existing = CartItem.objects.filter(cart=cart, product=product).first()
        else:
            existing = CartItem.objects.filter(cart=cart, package=package).first()

        if existing:
            existing.quantity += quantity
            existing.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product=product,
                package=package,
                quantity=quantity,
            )

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    permission_classes = [IsPatientUser]

    def patch(self, request, item_id):
        patient = request.user.patient_profile
        try:
            cart = Cart.objects.get(patient=patient)
            item = CartItem.objects.get(cart_item_id=item_id, cart=cart)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item.quantity = serializer.validated_data['quantity']
        item.save()
        return Response(CartSerializer(cart).data)


class RemoveCartItemView(APIView):
    permission_classes = [IsPatientUser]

    def delete(self, request, item_id):
        patient = request.user.patient_profile
        try:
            cart = Cart.objects.get(patient=patient)
            item = CartItem.objects.get(cart_item_id=item_id, cart=cart)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(CartSerializer(cart).data)


class CheckoutView(APIView):
    permission_classes = [IsPatientUser]

    def post(self, request):
        patient = request.user.patient_profile
        try:
            cart = Cart.objects.get(patient=patient)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        items = cart.items.select_related('product', 'package').all()
        if not items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        for item in items:
            if item.product:
                total_price += item.product.price * item.quantity
            elif item.package:
                total_price += item.package.price * item.quantity

        order = Order.objects.create(
            patient=patient,
            total_price=total_price,
            status='pending',
        )

        for item in items:
            unit_price = item.product.price if item.product else item.package.price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                package=item.package,
                quantity=item.quantity,
                price=unit_price,
            )

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
