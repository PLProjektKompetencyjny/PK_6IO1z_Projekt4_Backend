
class PG_check_translation:
    __constraints = {
        
        # User_Account
        "e_mail_chk": "E-mail address contains prohibited characters",
        "user_name_chk": "Username contains prohibited characters",
        "e_mail_or_user_name_chk": "Username and E-mail can not be NULL at the same time",
        
        # User_Details
        "nip_num_chk": "Invalid NIP number",
        "name_chk": "Invalid name",
        "surname_chk": "Invalid surname",
        "phone_num_chk": "Invalid phone number",
        "city_chk": "Invalid city",
        "postal_code_chk": "Invalid postal code",
        "street_chk": "Invalid street",
        "building_num_chk": "Invalid building number",
        
        # Reservation
        "start_date_chk": "Reservation start date can not be older than now",
        "end_date_chk": "Reservation end date can not be older than now",
        "reservation_dates_chk": "Reservation end date can not be older than start date",
        
        # Reservation_Room
        "num_of_adults_chk": "You can not book a room without adult",
        "num_of_children_chk": "Number of children can not be less than 0",

        
        # Invoice
        "price_gross_chk": "Invoice price must be greater than 0",
        
        # Room
        "room_price_gross_chk": "Room price must be greater than 0",
        
        # Room_Type
        "num_of_single_beds_chk": "Number of single beds can not be less than 0",
        "num_of_double_beds_chk": "Number of double beds can not be less than 0",
        "num_of_child_beds_chk": "Number of child beds can not be less than 0",
        "adult_price_gross_chk": "Adult price gross must be greater than 0",
        "child_price_gross_chk": "Child price gross can not be less than 0",
        
        # Service
        "Unit_price_chk": "Unit price must be greater than 0"

    }
    
    __default_message = "Form contains errors, fix them before submitting"
    

    @staticmethod
    def getMessage(constraint_name: str) -> str:
        return (
            PG_check_translation
            .__constraints.get(
                constraint_name,
                PG_check_translation.__default_message
            )
        )