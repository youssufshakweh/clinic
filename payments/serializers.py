from rest_framework import serializers
from .models import Payment, Cart, CartItem, Order, OrderItem, PaymentTransaction
from nutritionists.models import Product
from subscriptions.models import Package


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'payment_id',
            'patient',
            'appointment',
            'nutritionist',
            'amount',
            'date',
            'time',
            'status',
            'type',
            'payment_method',
            'transaction_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['payment_id', 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'product', 'package', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['cart_id', 'items', 'created_at']


class AddToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=False, allow_null=True
    )
    package = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all(), required=False, allow_null=True
    )
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, data):
        product = data.get('product')
        package = data.get('package')
        if product and package:
            raise serializers.ValidationError('Provide either product or package, not both.')
        if not product and not package:
            raise serializers.ValidationError('Provide either product or package.')
        return data


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'product', 'package', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'items', 'total_price', 'status', 'created_at']


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'items', 'total_price', 'status', 'created_at']
        read_only_fields = ['order_id', 'total_price', 'status', 'created_at']


class PaymentTransactionSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )

    class Meta:
        model = PaymentTransaction
        fields = ['id', 'transaction_id', 'order_id', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']
