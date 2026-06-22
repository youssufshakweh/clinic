from typing import Any

from dateutil.relativedelta import relativedelta
from django.db.models import F, QuerySet, Sum
from django.utils import timezone

from .models import OrderItem


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