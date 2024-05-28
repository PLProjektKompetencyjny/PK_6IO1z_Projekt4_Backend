
class PGFkeyTranslation:
    __constraints = {
        
        # Reservation_service
        "reservation_service": {
            "reservation_fkey": "Reservation with this ID does not exist",
            "service_fkey": "Service with this ID does not exist"
        },
        
        # User_details
        "user_details": {
            "user_fkey": "Contact details must be linked with existing user account",
            "last_modified_by_fkey": "Last modified by must be valid account ID"
        },
        
        # Reservation
        "reservation": {
            "user_fkey": "Reservation must be linked with existing user account",
            "status_fkey": "Reservation status does not exist",
            "last_modified_by_fkey": "Last modified by must be valid account ID"
        },
        
        # Reservation_room
        "reservation_room": {
            "reservation_fkey": "Reservation with this ID does not exist",
            "room_fkey": "Room with this ID does not exist",
            "room_status_fkey": "Reservation room status does not exist"
        },
        
        # Room
        "room": {
            "status_fkey": "Room status does not exist",
            "type_fkey": "Room type does not exist",
            "last_modified_by_fkey": "Last modified by must be valid account ID"
        },
        
        # Room_type
        "room_type": {
            "last_modified_by_fkey": "Last modified by must be valid account ID"
        },
        
        # Invoice
        "invoice": {
            "reservation_fkey": "Reservation with this ID does not exist",
            "Status_fkey": "Invoice status does not exist",
            "last_modified_by_fkey": "Last modified by must be valid account ID"
        },
        
        # User_account
        "user_account": {
            "last_modified_by_fkey": "Last modified by must be valid account ID"
        },
        
        # Service
        "service":{
            "last_modified_by_fkey": "Last modified by must be valid account ID"
        }
    }
    
    __default_message = "Can not be added"
    

    @staticmethod
    def getMessage(table_name: str, constraint_name: str) -> str:
        f_keys = PGFkeyTranslation.__constraints.get(
            table_name,
            None
        )
        if f_keys is not None:
            return (
                    f_keys.get(
                    constraint_name,
                    PGFkeyTranslation.__default_message
                )
            )
        else:
            return (
                PGFkeyTranslation.__default_message
            )