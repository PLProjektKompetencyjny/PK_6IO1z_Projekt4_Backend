
class PGUniqueTranslation:
    __constraints = {
        
        # User_account
        "user_account_pkey": "User with this ID already exists",
        "user_account_user_name_key": "Username is busy",
        "user_account_e_mail_key": "E-mail is busy",
        
        # User_Details
        "user_detail_user_id_key": "User with this ID already have details",
        
        # Reservation
        "reservation_pkey": "Reservation with this ID already exists",
        
        # Reservation_room
        "reservation_room_pkey": "This room is already assigned to this reservation",
        
        # Invoice
        "invoice_pkey": "Invoice with this ID already exists",
        "invoice_reservation_id_key": "Reservation with this ID has invoice",
        
        # Room
        "room_pkey": "Room with this ID already exists",
        
        # Room_type
        "room_type_pkey": "Room type with this ID already exists",
        
        # Service
        "service_pkey": "Service with this ID already exists",
        "service_name_key": "Service with this name already exists",
        
        # Reservation_service
        "reservation_service_pkey": "This service is already assigned to this reservation"
        
    }
    
    __default_message = "Can not be added"
    

    @staticmethod
    def getMessage(constraint_name: str) -> str:
        return (
            PGUniqueTranslation
            .__constraints.get(
                constraint_name,
                PGUniqueTranslation.__default_message
            )
        )