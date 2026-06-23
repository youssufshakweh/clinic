from enum import Enum


class AppointmentStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    NO_SHOW = 'no-show'


class AppointmentType(Enum):
    ONLINE = 'online'
    IN_PERSON = 'in-person'