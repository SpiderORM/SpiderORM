from MySQLdb import connect, OperationalError

__all__ = ['MysqlConnection']

class MysqlConnection:
    """
    A class to manage MySQL database connections.

    This class handles the connection to a MySQL database, including creating the database if it does not exist.

    Attributes:
        conn (MySQLdb.connections.Connection): The MySQL database connection object.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the MysqlConnection object.

        Tries to establish a connection to the specified MySQL database. If the database does not exist,
        it creates the database and then re-establishes the connection.

        Parameters:
            *args: Positional arguments passed to the MySQLdb `connect` method.
            **kwargs: Keyword arguments passed to the MySQLdb `connect` method. Common parameters include:
                - host (str): The hostname of the MySQL server.
                - user (str): The username to authenticate with.
                - password (str): The password to authenticate with.
                - database/db (str): The name of the database to connect to.
        """
        self.conn = None
        try:
            self.conn = connect(*args, **kwargs)
        except OperationalError as e:
            database = kwargs.get('database') or kwargs.get('db')
            _conn = connect(host=kwargs.get('host'), user=kwargs.get('user'), password=kwargs.get('password'))
            _conn.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {database};')
            _conn.commit()
            _conn.close()
        finally:
            self.conn = connect(*args, **kwargs)

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Returns a MySQL cursor object that can be used to execute queries.

        Returns:
            MySQLdb.cursors.Cursor: A cursor object to interact with the MySQL database.
        """
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Exit the runtime context related to this object.

        Commits the transaction and closes the MySQL database connection.

        Parameters:
            exc_type (type): The exception type.
            exc_value (Exception): The exception instance.
            exc_tb (traceback): The traceback object.
        """
        self.conn.commit()
        self.conn.close()
