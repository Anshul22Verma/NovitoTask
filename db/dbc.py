import sqlite3


class DataBaseConnection:
    def __init__(self, db_file: str) -> None:
        self.file = db_file
        self.connect()

    def connect(self) -> None:
        self.sqliteConnection = sqlite3.connect(self.file)
        # choosing to keep the connection opne 
        self.cursor = self.sqliteConnection.cursor()

    def query(self, query: str) -> None:
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print("Oops! ", e.__class__, " occurred.")
            print(f'error: {e}')
    
    def close(self) -> None:
        self.sqliteConnection.commit()
        self.cursor.close()
