from enum import Enum


class ReservationStatus(Enum):
    WAITING_CONFIRMATION = 1
    WAITING_PAYMENT = 2
    CONFIRMED = 3
    CANCELLED = 4
    CHECKED_IN = 5
    CHECKED_OUT = 6
    NO_SHOW = 7
