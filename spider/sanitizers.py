import re
from decimal import Decimal
from datetime import datetime
from html import escape
from spider.validators._re import verify_url_pattern

def sanitize_string(value):
    """
    Sanitize a string by removing non-alphanumeric characters and escaping HTML.

    Args:
    - value (str): The string to be sanitized.

    Returns:
    - str: The sanitized string.
    """
    sanitized_value = re.sub(r'[^\W\S]', '', value)
    return escape(sanitized_value)

def sanitize_integer(value):
    """
    Convert a value to an integer.

    Args:
    - value (str): The value to be converted.

    Returns:
    - int: The integer value.

    Raises:
    - ValueError: If the value cannot be converted to an integer.
    """
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid integer value: {value}.")

def sanitize_float(value):
    """
    Convert a value to a float.

    Args:
    - value (str): The value to be converted.

    Returns:
    - float: The float value.

    Raises:
    - ValueError: If the value cannot be converted to a float.
    """
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid float value: {value}.")

def sanitize_decimal(value):
    """
    Convert a value to a Decimal.

    Args:
    - value (str): The value to be converted.

    Returns:
    - Decimal: The Decimal value.

    Raises:
    - ValueError: If the value cannot be converted to a Decimal.
    """
    try:
        return Decimal(value)
    except ValueError:
        raise ValueError(f"Invalid decimal value: {value}.")

def sanitize_boolean(value):
    """
    Convert a value to a boolean.

    Args:
    - value (str or bool): The value to be converted.

    Returns:
    - bool: The boolean value.

    Raises:
    - ValueError: If the value cannot be converted to a boolean.
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ['true', '1', 'yes']:
        return True
    elif value.lower() in ['false', '0', 'no', 'not']:
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}.")

def sanitize_date(value):
    """
    Convert a value to a date.

    Args:
    - value (str): The value to be converted. Should be in "YYYY-MM-DD" format.

    Returns:
    - datetime.date: The date value.

    Raises:
    - ValueError: If the value cannot be converted to a date.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date value: {value}.")

def sanitize_datetime(value):
    """
    Convert a value to a datetime.

    Args:
    - value (str): The value to be converted. Should be in "YYYY-MM-DD HH:MM:SS" format.

    Returns:
    - datetime.datetime: The datetime value.

    Raises:
    - ValueError: If the value cannot be converted to a datetime.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"Invalid datetime value: {value}.")

def sanitize_time(value):
    """
    Convert a value to a time.

    Args:
    - value (str): The value to be converted. Should be in "HH:MM:SS" format.

    Returns:
    - datetime.time: The time value.

    Raises:
    - ValueError: If the value cannot be converted to a time.
    """
    try:
        return datetime.strptime(value, "%H:%M:%S").time()
    except ValueError:
        raise ValueError(f"Invalid time value: {value}.")

def sanitize_choice(value, choices):
    """
    Validate if the value is in the list of choices.

    Args:
    - value (str): The value to be validated.
    - choices (list): The list of valid choices.

    Returns:
    - str: The validated value.

    Raises:
    - ValueError: If the value is not in the list of choices.
    """
    if value in choices:
        return value
    else:
        raise ValueError(f"Invalid choice value: {value}.")

def sanitize_url(value):
    """
    Validate if the value is a valid URL.

    Args:
    - value (str): The URL to be validated.

    Returns:
    - str: The validated URL.

    Raises:
    - ValueError: If the URL is not valid.
    """
    if verify_url_pattern(value):
        return value
    else:
        raise ValueError(f"Invalid URL value: {value}.")

def sanitize_file(value, allowed_types):
    """
    Validate if the file type is allowed based on its extension.

    Args:
    - value (str): The file name.
    - allowed_types (list): List of allowed file extensions.

    Returns:
    - str: The validated file name.

    Raises:
    - ValueError: If the file type is not allowed.
    """
    if value.split('.')[-1] in allowed_types:
        return value
    else:
        raise ValueError(f"Invalid file type: {value}.")

def sanitize_image(value):
    """
    Validate if the file is an image based on its extension.

    Args:
    - value (str): The image file name.

    Returns:
    - str: The validated image file name.

    Raises:
    - ValueError: If the file is not a valid image type.
    """
    if value.split('.')[-1] in ['png', 'jpg', 'gif']:
        return value
    else:
        raise ValueError(f"Invalid image value: {value}.")
