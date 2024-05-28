from src.utils.PostgreSQL_errors.pg_error_codes import PG_ErrorsCodes
from src.utils.PostgreSQL_errors.describe_pg_check import PG_check_translation
from src.utils.PostgreSQL_errors.describe_pg_unique import PG_unique_translation
from src.utils.PostgreSQL_errors.describe_pg_fkey import PG_fkey_translation
from src.utils.PostgreSQL_errors.describe_pg_not_nullable import PG_not_nullable_translation
from src.utils.PostgreSQL_errors.describe_pg_custom import PG_custom_translation


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
        
        if PG_ErrorsCodes.NotNullViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PG_ErrorsCodes.getErrorType(error_code),
                PG_not_nullable_translation.getMessage(
                    PostgresErrorHandler.getColumnName(e),
                    PostgresErrorHandler.getTableName(e)
                ),
                error_code
            )

        elif PG_ErrorsCodes.ForeignKeyViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PG_ErrorsCodes.getErrorType(error_code),
                PG_fkey_translation.getMessage(
                    PostgresErrorHandler.getTableName(e),
                    PostgresErrorHandler.getConstraintName(e)
                ),
                error_code
            )

        elif PG_ErrorsCodes.UniqueViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PG_ErrorsCodes.getErrorType(error_code),
                PG_unique_translation.getMessage(
                    PostgresErrorHandler.getConstraintName(e)
                ),
                error_code
            )

        elif PG_ErrorsCodes.CheckViolation == error_code:
            return PostgresErrorHandler.__format_error_info(
                PG_ErrorsCodes.getErrorType(error_code),
                PG_check_translation.getMessage(
                    PostgresErrorHandler.getConstraintName(e)
                ),
                error_code
            )
            
        elif error_code in PG_ErrorsCodes.getCustomCode():
            return PostgresErrorHandler.__format_error_info(
                PG_ErrorsCodes.getErrorType(error_code),
                PG_custom_translation.getMessage(error_code),
                error_code
            )
            
        else:
            return PostgresErrorHandler.__format_error_info(
                PG_ErrorsCodes.getDefaultCategory(),
                PostgresErrorHandler.getPrimaryMessage(e),
                error_code
            )
