from enum import Enum


class InvoiceStatus(Enum):
    DRAFT = 1
    SENT = 2
    WAITING_PAYMENT = 3
    PAID = 4
    CANCELLED = 5
    CORRECTION = 6
