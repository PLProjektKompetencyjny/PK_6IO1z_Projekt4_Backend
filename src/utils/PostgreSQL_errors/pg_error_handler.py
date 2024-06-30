from src.utils.PostgreSQL_errors.pg_error_codes import PGErrorsCodes
from src.utils.PostgreSQL_errors.describe_pg_check import PGCheckTranslation
from src.utils.PostgreSQL_errors.describe_pg_unique import PGUniqueTranslation
from src.utils.PostgreSQL_errors.describe_pg_fkey import PGFkeyTranslation
from src.utils.PostgreSQL_errors.describe_pg_not_nullable import PGNotNullableTranslation
from src.utils.PostgreSQL_errors.describe_pg_custom import PGCustomTranslation


class PostgresErrorHandler:

    @staticmethod
    def __format_error_info(type: str, message: str, code: str) -> dict[str, str]:
        return {
            "type": type,
            "message": message,
            "code": code
        }

    @staticmethod
    def getErrorCode(e) -> str:
        return str(e.orig.pgcode)

    @staticmethod
    def getPrimaryMessage(e) -> str:
        return str(e.orig.diag.message_primary)

    @staticmethod
    def getMessageDetail(e) -> str:
        return str(e.orig.diag.message_primary)

    @staticmethod
    def getConstraintName(e) -> str:
        return str(e.orig.diag.constraint_name)

    @staticmethod
    def getTableName(e) -> str:
        return str(e.orig.diag.table_name)

    @staticmethod
    def getColumnName(e) -> str:
        return str(e.orig.diag.column_name)

    @staticmethod
    def getErrorInfo(e) -> dict[str, str]:
        
        error_code = PostgresErrorHandler.getErrorCode(e)
        
        if PGErrorsCodes.NotNullViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PGErrorsCodes.getErrorType(error_code),
                PGNotNullableTranslation.getMessage(
                    PostgresErrorHandler.getColumnName(e),
                    PostgresErrorHandler.getTableName(e)
                ),
                error_code
            )

        elif PGErrorsCodes.ForeignKeyViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PGErrorsCodes.getErrorType(error_code),
                PGFkeyTranslation.getMessage(
                    PostgresErrorHandler.getTableName(e),
                    PostgresErrorHandler.getConstraintName(e)
                ),
                error_code
            )

        elif PGErrorsCodes.UniqueViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PGErrorsCodes.getErrorType(error_code),
                PGUniqueTranslation.getMessage(
                    PostgresErrorHandler.getConstraintName(e)
                ),
                error_code
            )

        elif PGErrorsCodes.CheckViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PGErrorsCodes.getErrorType(error_code),
                PGCheckTranslation.getMessage(
                    PostgresErrorHandler.getConstraintName(e)
                ),
                error_code
            )
            
        elif error_code in PGErrorsCodes.getCustomCode():
            return PostgresErrorHandler.__format_error_info(
                PGErrorsCodes.getErrorType(error_code),
                PGCustomTranslation.getMessage(error_code),
                error_code
            )
            
        else:
            return PostgresErrorHandler.__format_error_info(
                PGErrorsCodes.getDefaultCategory(),
                PostgresErrorHandler.getPrimaryMessage(e),
                error_code
            )
