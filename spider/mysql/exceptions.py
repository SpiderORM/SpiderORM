class MysqlConnectionError(Exception):
    """
    Custom exception for errors related to MySQL connections.

    This exception is raised when an error specific to MySQL connections occurs.

    Args:
        message (str): The error message to be displayed.
    """

    def __init__(self, message) -> None:
        """
        Initialize the MysqlConnectionError with a specific error message.

        Args:
            message (str): The error message to be passed to the exception.
        """
        super().__init__(message)
