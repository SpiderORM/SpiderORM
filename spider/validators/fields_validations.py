from decimal import Decimal
from datetime import date, datetime, time

from spider.validators.exceptions import ValidationError
from spider.validators._re import verify_email_pattern, verify_url_pattern
from spider.sanitizers import *


def validate_required(value):
    """
    Validate that the value is not None or an empty string.

    Args:
        value: The value to be validated.

    Raises:
        ValidationError: If the value is None or an empty string.
    """
    if value is None or value == '':
        raise ValidationError('This field is required.')


def validate_null(value):
    """
    Validate that the value is None or not an empty string.

    Args:
        value: The value to be validated.

    Raises:
        ValidationError: If the value is not None and is an empty string.
    """
    if value is not None and value == '':
        raise ValidationError('This field can’t be null.')


def validate_string(value, max_length=None):
    """
    Validate that the value is a string and optionally checks its length.

    Args:
        value: The value to be validated.
        max_length (int, optional): The maximum allowed length of the string.

    Returns:
        str: The sanitized string value.

    Raises:
        ValidationError: If the value is not a string or exceeds the maximum length.
    """
    value = sanitize_string(value)
    if not isinstance(value, str):
        raise ValidationError(f"Value must be a string: {value}.")
    if max_length and len(value) > max_length:
        raise ValidationError(f"Value exceeds maximum length of {max_length}.")
    return value


def validate_integer(value):
    """
    Validate that the value is an integer.

    Args:
        value: The value to be validated.

    Returns:
        int: The sanitized integer value.

    Raises:
        ValidationError: If the value is not an integer.
    """
    value = sanitize_integer(value)
    if not isinstance(value, int):
        raise ValidationError(f"Value must be an integer: {value}.")
    return value


def validate_float(value):
    """
    Validate that the value is a float.

    Args:
        value: The value to be validated.

    Returns:
        float: The sanitized float value.

    Raises:
        ValidationError: If the value is not a float.
    """
    value = sanitize_float(value)
    if not isinstance(value, float):
        raise ValidationError(f"Value must be a float: {value}.")
    return value


def validate_decimal(value):
    """
    Validate that the value is a Decimal.

    Args:
        value: The value to be validated.

    Returns:
        Decimal: The sanitized Decimal value.

    Raises:
        ValidationError: If the value is not a Decimal.
    """
    value = sanitize_decimal(value)
    if not isinstance(value, Decimal):
        raise ValidationError(f"Value must be a decimal.")
    return value


def validate_boolean(value):
    """
    Validate that the value is a boolean.

    Args:
        value: The value to be validated.

    Returns:
        bool: The sanitized boolean value.

    Raises:
        ValidationError: If the value is not a boolean.
    """
    if not isinstance(value, bool):
        raise ValidationError(f"Value must be a boolean: {value}.")
    value = sanitize_boolean(value)
    return value


def validate_date(value):
    """
    Validate that the value is a date.

    Args:
        value: The value to be validated.

    Returns:
        date: The sanitized date value.

    Raises:
        ValidationError: If the value is not a date.
    """
    value = sanitize_date(value)
    if not isinstance(value, date):
        raise ValidationError(f"Value must be a date: {value}.")
    return value


def validate_datetime(value):
    """
    Validate that the value is a datetime.

    Args:
        value: The value to be validated.

    Returns:
        datetime: The sanitized datetime value.

    Raises:
        ValidationError: If the value is not a datetime.
    """
    value = sanitize_datetime(value)
    if not isinstance(value, datetime):
        raise ValidationError(f"Value must be a datetime: {value}.")
    return value


def validate_time(value):
    """
    Validate that the value is a time.

    Args:
        value: The value to be validated.

    Returns:
        time: The sanitized time value.

    Raises:
        ValidationError: If the value is not a time.
    """
    value = sanitize_time(value)
    if not isinstance(value, time):
        raise ValidationError(f"Value must be a time: {value}.")
    return value


def validate_choices(value, choices):
    """
    Validate that the value is within the allowed choices.

    Args:
        value: The value to be validated.
        choices (iterable): A list or tuple of allowed choices.

    Returns:
        str: The sanitized string value.

    Raises:
        ValidationError: If the value is not in the allowed choices.
    """
    value = sanitize_string(value)
    if value not in choices:
        raise ValidationError(f"Value must be one of {choices}.")
    return value


def validate_url(value):
    """
    Validate that the value is a valid URL.

    Args:
        value: The value to be validated.

    Returns:
        str: The sanitized URL value.

    Raises:
        ValidationError: If the value is not a valid URL.
    """
    value = sanitize_url(value)
    if not value:
        raise ValidationError(f"Value must be a URL.")
    return value


def validate_file_type(value, allowed_types):
    """
    Validate that the file type is one of the allowed types.

    Args:
        value: The file name or path to be validated.
        allowed_types (list): A list of allowed file extensions.

    Returns:
        str: The sanitized file name or path.

    Raises:
        ValidationError: If the file type is not in the allowed types.
    """
    value = sanitize_file(value)
    if not any(value.endswith(allowed_type) for allowed_type in allowed_types):
        raise ValidationError(f"Value must be one of {allowed_types}.")
    return value


def validate_default(value, default):
    """
    Return the default value if the given value is None.

    Args:
        value: The value to be checked.
        default: The default value to return if value is None.

    Returns:
        The original value if not None, otherwise the default value.
    """
    return value if value is not None else default


def validate_email(value):
    """
    Validate that the value is a valid email address.

    Args:
        value: The value to be validated.

    Returns:
        str: The sanitized email value.

    Raises:
        ValidationError: If the value does not match the email pattern.
    """
    value = sanitize_string(value)
    if not verify_email_pattern(value):
        raise ValidationError(f"Value doesn't match the email pattern.")
    return value


def validate_password(value, hash, salt, max_length):
    """
    Validate that the password meets certain criteria.

    Args:
        value: The password string to be validated.
        hash (str): The hashing algorithm to be used.
        salt (bytes): A salt value for the password hashing.
        max_length (int): The maximum allowed length of the password.

    Returns:
        str: The sanitized password value.

    Raises:
        ValidationError: If the hash algorithm is not available, if the password exceeds max_length, or if the salt is not bytes.
    """
    from hashlib import algorithms_available

    value = sanitize_string(value)
    validate_choices(hash, choices=list(algorithms_available))
    validate_string(value, max_length)
    if not isinstance(salt, bytes):
        raise ValidationError(f"salt must be a bytes instance.")
    return value
