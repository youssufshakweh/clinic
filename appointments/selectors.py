from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet, Count
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractYear
from django.utils import timezone

from .constants import AppointmentStatus, AppointmentType
from .models import Appointment


def get_appointments(options: dict[str, any] | None = None) -> QuerySet[Appointment]:
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


def get_total_completed_appointments(appointment_type: str | None = None) -> int:
    """Get total count of completed appointments, optionally filtered by type."""
    options = {'status': AppointmentStatus.COMPLETED.value}
    if appointment_type:
        options['type'] = appointment_type
    return get_appointments(options).count()


def get_most_booking_weekday(appointment_type: str | None = None) -> dict:
    """Get the weekday with the most bookings, optionally filtered by type."""
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    options = {'status': AppointmentStatus.COMPLETED.value}
    if appointment_type:
        options['type'] = appointment_type
    
    queryset = get_appointments(options)
    
    # Annotate with weekday and count
    result = queryset.annotate(
        weekday=ExtractWeekDay('date')
    ).values('weekday').annotate(
        count=Count('app_id')
    ).order_by('-count')
    
    if not result:
        return {'day_id': 0, 'day_name': 'Monday'}
    
    # ExtractWeekDay returns 1=Sunday, 2=Monday, ..., 7=Saturday
    # We need to convert to 0=Monday, 1=Tuesday, ..., 6=Sunday
    most_booked = result.first()
    db_weekday = most_booked['weekday']  # 1-7 where 1=Sunday
    
    # Convert to our format (0=Monday, 6=Sunday)
    our_weekday = (db_weekday - 2) % 7  # Monday=0, Tuesday=1, ..., Sunday=6
    
    return {
        'day_id': our_weekday,
        'day_name': weekday_names[our_weekday]
    }


def get_appointments_by_period(groupby: str, appointment_type: str | None = None, year: int | None = None, month: int | None = None, week: int | None = None) -> list:
    """
    Get appointments grouped by time period with gap filling.
    
    Args:
        groupby: 'weekday', 'month', or 'year'
        appointment_type: Optional filter by appointment type
        year: Optional filter by year
        month: Optional filter by month
        week: Optional filter by week
        
    Returns:
        List of dicts with period info and counts
    """
    from utils.gap import fill_weekday_gaps, fill_month_gaps, fill_year_gaps
    
    options = {'status': AppointmentStatus.COMPLETED.value}
    if appointment_type:
        options['type'] = appointment_type
    if year:
        options['date__year'] = year
    if month:
        options['date__month'] = month
    if week:
        options['date__week'] = week
    
    queryset = get_appointments(options)
    
    if groupby == 'weekday':
        # Group by weekday (0=Monday, 6=Sunday in our format)
        result = queryset.annotate(
            weekday=ExtractWeekDay('date')
        ).values('weekday').annotate(
            count=Count('app_id')
        )
        
        # Convert ExtractWeekDay (1=Sunday to 7=Saturday) to our format (0=Monday to 6=Sunday)
        data = []
        for item in result:
            db_weekday = item['weekday']
            our_weekday = (db_weekday - 2) % 7
            data.append({'weekday': our_weekday, 'count': item['count']})
        
        return fill_weekday_gaps(data)
    
    elif groupby == 'month':
        # Group by month
        result = queryset.annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(
            count=Count('app_id')
        )
        
        data = [{'month': item['month'], 'count': item['count']} for item in result]
        return fill_month_gaps(data, year=year)
    
    elif groupby == 'year':
        # Group by year
        result = queryset.annotate(
            year=ExtractYear('date')
        ).values('year').annotate(
            count=Count('app_id')
        )
        
        data = [{'year': item['year'], 'count': item['count']} for item in result]
        return fill_year_gaps(data)
    
    return []