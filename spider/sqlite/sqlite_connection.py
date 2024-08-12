import sqlite3

class SQLIteConnection:
    """
    Context manager class for handling SQLite database connections.

    This class manages the connection to an SQLite database, ensuring that the connection is properly opened and closed,
    and that any changes are committed.

    Attributes:
        conn (sqlite3.Connection): The SQLite connection object.
        cursor (sqlite3.Cursor): The SQLite cursor object for executing SQL commands.
    """

    def __enter__(self) -> sqlite3.Cursor:
        """
        Enter the runtime context for the SQLite connection.

        Establishes a connection to the SQLite database and returns a cursor object for executing SQL queries.

        Returns:
            sqlite3.Cursor: The cursor object to execute SQL queries.
        """
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the runtime context for the SQLite connection.

        Commits any changes made during the session and closes the database connection.

        Args:
            exc_type (type): The exception type, if an exception was raised.
            exc_val (Exception): The exception instance, if an exception was raised.
            exc_tb (traceback): The traceback object, if an exception was raised.
        """
        self.conn.commit()
        self.conn.close()
