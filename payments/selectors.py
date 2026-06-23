from typing import Any

from dateutil.relativedelta import relativedelta
from django.db.models import F, QuerySet, Sum
from django.utils import timezone

from .models import OrderItem
from nutritionists.models import Product


def get_order_items(options: dict[str, Any] | None = None) -> QuerySet[OrderItem]:
    if not options:
        options = {}

    return OrderItem.objects.filter(**options)


def get_total_product_profit() -> float:
    total_prices = get_order_items({'product__isnull': False, 'order__status': 'confirmed'}).annotate(
        total_price=Sum(F("quantity") * F("price")
        )
    ).values_list("total_price", flat=True)
    return float(sum(total_prices))


def get_total_product_profit_for_current_month() -> float:
    curr_date = timezone.now().date()
    curr_year = curr_date.year
    curr_month = curr_date.month

    total_prices = get_order_items({'product__isnull': False, 'order__created_at__year': curr_year, 'order__created_at__month': curr_month, 'order__status': 'confirmed'}).annotate(
        total_price=Sum(F("quantity") * F("price")
        )
    ).values_list("total_price", flat=True)
    return float(sum(total_prices))


def get_total_product_profit_for_previous_month() -> float:
    curr_date = timezone.now().date()
    prev_month_date = curr_date - relativedelta(months=1)
    prev_year = prev_month_date.year
    prev_month = prev_month_date.month

    total_prices = get_order_items({'product__isnull': False, 'order__created_at__year': prev_year, 'order__created_at__month': prev_month, 'order__status': 'confirmed'}).annotate(
        total_price=Sum(F("quantity") * F("price")
        )
    ).values_list("total_price", flat=True)
    return float(sum(total_prices))


def get_best_selling_product() -> dict | None:
    best_selling = get_order_items({'product__isnull': False, 'order__status': 'confirmed'}).values(
        'product__product_id',
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity').first()

    if not best_selling:
        return None

    return {
        'product_id': best_selling['product__product_id'],
        'product_name': best_selling['product__name'],
        'total_quantity': best_selling['total_quantity']
    }


def get_product_revenue_distribution() -> list[dict]:
    products = Product.objects.all()
    revenue_data = []

    for product in products:
        total_revenue = get_order_items({
            'product': product,
            'order__status': 'confirmed'
        }).annotate(
            item_revenue=Sum(F("quantity") * F("price"))
        ).values_list("item_revenue", flat=True)

        revenue_sum = float(sum(total_revenue)) if total_revenue else 0.0

        revenue_data.append({
            'product_id': product.product_id,
            'product_name': product.name,
            'total_revenue': revenue_sum
        })

    return revenue_data