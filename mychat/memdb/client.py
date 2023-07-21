import psycopg2

MEMORY_TABLE_NAME = "memories"

class MemoryDBClient:
    
    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
            database_name: str
        ) -> None:
        
        self._connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database_name,
        )
        
        self._cursor = self._connection.cursor()
    
    def create_memory_table(self):
        
        self._cursor.execute(
            """CREATE TABLE IF NOT EXSITS {table_name} (
                id SERIAL PRIMARY KEY,
                content VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL
            )
            """.format(
                table_name=MEMORY_TABLE_NAME
            )
        )