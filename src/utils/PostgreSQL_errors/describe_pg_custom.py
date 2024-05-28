
class PG_custom_translation:
    __constraints = {
        
        "23515": "Room is unavailable in selected time frame",
        "23516": "E-mail address can not be set as username",
        "23517": "User account without username can not be promoted to admin account",
        "23518": "Too many people assigned to room",
        "23518": "Invalid username or password",
        "23519": "User is not active",
        "23520": "Cannot Change Password. Invalid username or password",
        "23998": "No Operation has been performed",
        "23999": "Operation not permitted",
        
    }
    
    __default_message = "unknown error"
    

    @staticmethod
    def getMessage(err_code: str) -> str:
        return (
            PG_custom_translation
            .__constraints.get(
                err_code,
                PG_custom_translation.__default_message
            )
        )