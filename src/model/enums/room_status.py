from enum import Enum


class RoomStatus(Enum):
    AVAILABLE = 1
    OCCUPIED = 2
    RESERVED = 3
    OUT_OF_ORDER = 4
    MAINTENANCE = 5
