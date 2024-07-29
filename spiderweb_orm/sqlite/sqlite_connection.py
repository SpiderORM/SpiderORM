import sqlite3


class SQLIteConnection:
    def __enter__(self) -> None:
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self,exc_type,exc_val,exc_to):
        self.conn.commit()
        self.conn.close()