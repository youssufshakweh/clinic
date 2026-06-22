from typing import Any

from django.db.models import QuerySet

from .models import Product


def get_products(options: dict[str, Any] | None = None) -> QuerySet[Product]:
    if not options:
        options = {}

    return Product.objects.filter(**options)


def get_count_of_low_stock_product() -> int:
    MIN_QUANTITY = 5

    return get_products({'quantity__lte': MIN_QUANTITY}).count()