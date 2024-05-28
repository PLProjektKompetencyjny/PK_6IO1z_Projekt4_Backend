class PGErrorsCodes:
    
    __categories = {
        "23502": "Not Nullable",
        "23503": "Item does not exist",
        "23505": "Value is not unique",
        "23514": "Value is not valid",
        "23515": "Room Unavailable",
        "23516": "Email to Username",
        "23517": "No Username Account",
        "23518": "Too Many People",
        "23518": "Cannot Authenticate User",
        "23519": "User is Not Active",
        "23520": "Cannot Change Password",
        "23998": "No Operation Performed",
        "23999": "Operation Not Permitted",
    }
    __standard_codes = ["23502", "23503", "23505", "23514"]
    
    __default_category = "Unknown"
    
    NotNullViolation = "23502"
    ForeignKeyViolation = "23503"
    UniqueViolation = "23505"
    CheckViolation = "23514"
    
    @staticmethod
    def getErrorType(error_code: str) -> str:
        return (
            PGErrorsCodes.__categories.get(
                error_code,
                PGErrorsCodes.__default_category
            )
        )
    
    @staticmethod
    def getCustomCode() -> list[str]:
        return [
            id for id in PGErrorsCodes.__categories.keys() 
            if id not in PGErrorsCodes.__standard_codes
        ]
        
    @staticmethod
    def getDefaultCategory() -> str:
        return PGErrorsCodes.__default_category