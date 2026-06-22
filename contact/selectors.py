from typing import Any

from django.db.models import QuerySet

from contact.models import Inquiry


def get_inquiries(options: dict[str, Any] | None = None) -> QuerySet[Inquiry]:
    if options is None:
        options = {}

    return Inquiry.objects.filter(**options)


def get_unread_inquiries_count() -> int:
    return get_inquiries({'is_read': False}).count()