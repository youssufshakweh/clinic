from typing import Any

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from django.utils import timezone

from .constants import AppointmentStatus
from .models import Appointment


def get_appointments(options: dict[str, Any] | None = None) -> QuerySet[Appointment]:
    if options is None:
        options = {}

    return Appointment.objects.filter(**options)

def get_incoming_appointments_for_today_count() -> int:
    today = timezone.localdate()
    return get_appointments({
        'date': today,
        'status': AppointmentStatus.CONFIRMED.value
    }).count()


def get_upcoming_appointments_for_today_count() -> int:
    today = timezone.localtime()
    return get_appointments({
        'date': today.date(),
        'time__gt': today.time(),
        'status': AppointmentStatus.CONFIRMED.value
    }).count()


def get_total_cancelled_appointments() -> int:
    return get_appointments({'status': AppointmentStatus.CANCELLED.value}).count()


def get_total_cancelled_appointments_for_current_month() -> int:
    curr_date = timezone.now().date()
    curr_year = curr_date.year
    curr_month = curr_date.month

    return get_appointments({'date__year': curr_year, 'date__month': curr_month, 'status': AppointmentStatus.CANCELLED.value}).count()


def get_total_cancelled_appointments_for_previous_month() -> int:
    curr_date = timezone.now().date()
    prev_month_date = curr_date - relativedelta(months=1)
    prev_year = prev_month_date.year
    prev_month = prev_month_date.month

    return get_appointments({'date__year': prev_year, 'date__month': prev_month, 'status': AppointmentStatus.CANCELLED.value}).count()