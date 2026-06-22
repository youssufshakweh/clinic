from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from django.utils import timezone

from .models import Patient


def get_patients(options: dict[str, any] | None = None) -> QuerySet[Patient]:
    if options is None:
        options = {}

    return Patient.objects.filter(**options)


def get_total_patients_count() -> int:
    return get_patients().count()


def get_total_patients_count_for_current_month() -> int:
    curr_date = timezone.now().date()
    curr_year = curr_date.year
    curr_month = curr_date.month

    return get_patients({'created_at__year': curr_year, 'created_at__month': curr_month}).count()


def get_total_patients_count_for_previous_month() -> int:
    curr_date = timezone.now().date()
    prev_month_date = curr_date - relativedelta(months=1)
    prev_year = prev_month_date.year
    prev_month = prev_month_date.month

    return get_patients({'created_at__year': prev_year, 'created_at__month': prev_month}).count()