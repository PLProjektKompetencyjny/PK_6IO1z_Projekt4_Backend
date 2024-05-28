class PG_ErrorsCodes:
    
    __categories = {
        "23502": "Nullability",
        "23503": "Relations",
        "23505": "Uniqueness",
        "23514": "Validation"
    }
    
    __default_category = "Unknown"
    
    NotNullViolation = "23502"
    ForeignKeyViolation = "23503"
    UniqueViolation = "23505"
    CheckViolation = "23514"
    
    @staticmethod
    def getErrorType(error_code: str) -> str:
        return (
            PG_ErrorsCodes.__categories.get(
                error_code,
                PG_ErrorsCodes.__default_category
            )
        )