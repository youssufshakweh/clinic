from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Order, OrderItem, PaymentTransaction
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    OrderListSerializer,
    PaymentTransactionSerializer,
)
from utils.pagination import StandardPagination
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

        appointment = serializer.validated_data.get('appointment')

        if appointment:
            if CartItem.objects.filter(cart=cart, appointment=appointment).exists():
                return Response(
                    {'error': 'هذا الموعد موجود بالفعل في السلة'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            CartItem.objects.create(cart=cart, appointment=appointment, quantity=1)
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

        if product:
            if quantity > product.quantity:
                return Response(
                    {'error': f'الكمية المطلوبة ({quantity}) تتجاوز المخزون المتاح ({product.quantity})'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            existing = CartItem.objects.filter(cart=cart, product=product).first()
            if existing and (existing.quantity + quantity) > product.quantity:
                return Response(
                    {'error': f'إجمالي الكمية في السلة ({existing.quantity + quantity}) يتجاوز المخزون المتاح ({product.quantity})'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
        return Response({"message": "Item removed"}, status=status.HTTP_200_OK)


class CheckoutView(APIView):
    permission_classes = [IsPatientUser]

    def post(self, request):
        patient = request.user.patient_profile
        try:
            cart = Cart.objects.get(patient=patient)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        items = cart.items.select_related('product', 'package', 'appointment').all()
        if not items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        from decimal import Decimal
        total_price = Decimal('0.00')
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
            if item.product:
                unit_price = item.product.price
            elif item.package:
                unit_price = item.package.price
            else:
                unit_price = Decimal('0.00')
            OrderItem.objects.create(
                order=order,
                product=item.product,
                package=item.package,
                appointment=item.appointment,
                quantity=item.quantity,
                price=unit_price,
            )
            if item.product:
                item.product.quantity -= item.quantity
                item.product.save()

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    permission_classes = [IsPatientUser]

    def get(self, request):
        patient = request.user.patient_profile
        orders = Order.objects.filter(patient=patient).order_by('-created_at')
        paginator = StandardPagination()
        page = paginator.paginate_queryset(orders, request)
        serializer = OrderListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SubmitTransactionView(APIView):
    permission_classes = [IsPatientUser]

    def post(self, request):
        serializer = PaymentTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.validated_data['order']
        patient = request.user.patient_profile
        if order.patient != patient:
            return Response(
                {'error': 'هذا الطلب لا يخصك'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if PaymentTransaction.objects.filter(transaction_id=serializer.validated_data['transaction_id']).exists():
            return Response(
                {'error': 'رقم المعاملة مستخدم مسبقاً'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction = PaymentTransaction.objects.create(
            transaction_id=serializer.validated_data['transaction_id'],
            user=request.user,
            order=order,
        )
        return Response(
            PaymentTransactionSerializer(transaction).data,
            status=status.HTTP_201_CREATED,
        )
