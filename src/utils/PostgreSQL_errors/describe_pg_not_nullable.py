
class PG_not_nullable_translation:
    __constraints = {
        
        "<table_name>":{
            "column_name_1": "Description for column 1 not null",
            "column_name_2": "Description for column 2 not null"
        }
    }
    

    @staticmethod
    def __getDefaultMessage(column_name: str, table_name: str) -> str:
        return (
            str(
                " ".join(
                    [
                        "Column",
                        column_name,
                        "in",
                        table_name,
                        "can not be null"
                    ]
                )
            )
        )
        
    @staticmethod
    def getMessage(column_name: str, table_name: str) -> str:
        nullable_columns = PG_not_nullable_translation.__constraints.get(
                table_name,
                None
            )
        
        if nullable_columns is not None:
            return (
                nullable_columns.get(
                    column_name,
                    PG_not_nullable_translation.__getDefaultMessage(
                        column_name,
                        table_name
                    )
                )
            )
        else:       
            return (
                PG_not_nullable_translation.__getDefaultMessage(
                    column_name,
                    table_name
                )
            )