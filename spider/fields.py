"""
This module handles various field types used for database models,
including validation and sanitization of different types of data.

Classes:
- Field: Base class for all field types, providing basic validation.
- CharField: Represents a string field with a maximum length.
- IntegerField: Represents an integer field, optionally with auto-increment.
- DecimalField: Represents a decimal field with precision and scale.
- FloatField: Represents a floating-point number field.
- BooleanField: Represents a boolean field.
- DateField: Represents a date field.
- DateTimeField: Represents a datetime field.
- TimeField: Represents a time field.
- ChoiceField: Represents a choice field with a set of predefined choices.
- ImageField: Represents an image file field.
- FileField: Represents a file field with allowed file types.
- URLField: Represents a URL field.
- ForeignKey: Represents a foreign key relationship to another model.
- TextField: Represents a text field for large text data.
- PasswordField: Represents a password field with hashing and salting.
- EmailField: Represents an email field.
- ManyToManyField: Represents a many-to-many relationship to another model.
"""

from spider.validators.fields_validations import (
    validate_boolean, validate_choices,
    validate_date, validate_datetime,
    validate_decimal, validate_default,
    validate_file_type, validate_float,
    validate_integer, validate_null,
    validate_string, validate_url,
    validate_email, validate_time,
    validate_password
)


class Field:
    """
    Base class for all field types.

    Attributes:
    - primary_key (bool): Indicates if this field is a primary key.
    - null (bool): Indicates if this field can be null.
    - default: Default value for the field if no value is provided.
    - unique (bool): Indicates if this field must have unique values.

    Methods:
    - validate(value): Validates the value according to field constraints.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None):
        self.primary_key = primary_key
        self.null = null
        self.default = default
        self.unique = unique

    def validate(self, value):
        """
        Validates the value based on field constraints.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated value.

        Raises:
        - ValidationError: If the value does not meet field constraints.
        """
        if self.null:
            validate_null(value)
        if self.default:
            validate_default(value, self.default)
        return value


class CharField(Field):
    """
    Represents a string field with a maximum length.

    Attributes:
    - max_length (int): Maximum length of the string.

    Methods:
    - validate(value): Validates the string value and checks length constraints.
    """

    def __init__(self, max_length, primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)
        self.max_length = max_length

    def validate(self, value):
        """
        Validates the string value and checks length constraints.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated string value.

        Raises:
        - ValidationError: If the value does not meet string constraints.
        """
        value = super().validate(value)
        value = validate_string(value, self.max_length)
        return value


class IntegerField(Field):
    """
    Represents an integer field, optionally with auto-increment.

    Attributes:
    - auto_increment (bool): Indicates if the field should auto-increment.

    Methods:
    - validate(value): Validates the integer value.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None, auto_increment=False):
        super().__init__(primary_key, null, unique, default)
        self.auto_increment = auto_increment

    def validate(self, value):
        """
        Validates the integer value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated integer value.

        Raises:
        - ValidationError: If the value is not a valid integer.
        """
        value = super().validate(value)
        value = validate_integer(value)
        return value


class DecimalField(Field):
    """
    Represents a decimal field with precision and scale.

    Attributes:
    - max_digits (int): Total number of digits.
    - decimal_places (int): Number of decimal places.

    Methods:
    - validate(value): Validates the decimal value.
    """

    def __init__(self, max_digits, decimal_places, primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)
        self.max_digits = max_digits
        self.decimal_places = decimal_places

    def validate(self, value):
        """
        Validates the decimal value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated decimal value.

        Raises:
        - ValidationError: If the value is not a valid decimal.
        """
        value = super().validate(value)
        value = validate_decimal(value)
        return value


class FloatField(Field):
    """
    Represents a floating-point number field.

    Methods:
    - validate(value): Validates the float value.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)

    def validate(self, value):
        """
        Validates the float value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated float value.

        Raises:
        - ValidationError: If the value is not a valid float.
        """
        value = super().validate(value)
        value = validate_float(value)
        return value


class BooleanField(Field):
    """
    Represents a boolean field.

    Methods:
    - validate(value): Validates the boolean value.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)

    def validate(self, value):
        """
        Validates the boolean value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated boolean value.

        Raises:
        - ValidationError: If the value is not a valid boolean.
        """
        value = super().validate(value)
        value = validate_boolean(value)
        return value


class DateField(Field):
    """
    Represents a date field.

    Attributes:
    - auto_now (bool): Indicates if the field should auto-update to the current date.

    Methods:
    - validate(value): Validates the date value.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None, auto_now=False):
        super().__init__(primary_key, null, unique, default)
        self.auto_now = auto_now

    def validate(self, value):
        """
        Validates the date value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated date value.

        Raises:
        - ValidationError: If the value is not a valid date.
        """
        value = super().validate(value)
        value = validate_date(value)
        return value


class DateTimeField(Field):
    """
    Represents a datetime field.

    Attributes:
    - auto_now (bool): Indicates if the field should auto-update to the current datetime.

    Methods:
    - validate(value): Validates the datetime value.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None, auto_now=False):
        super().__init__(primary_key, null, unique, default)
        self.auto_now = auto_now

    def validate(self, value):
        """
        Validates the datetime value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated datetime value.

        Raises:
        - ValidationError: If the value is not a valid datetime.
        """
        value = super().validate(value)
        value = validate_datetime(value)
        return value


class TimeField(Field):
    """
    Represents a time field.

    Attributes:
    - auto_now (bool): Indicates if the field should auto-update to the current time.

    Methods:
    - validate(value): Validates the time value.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None, auto_now=False):
        super().__init__(primary_key, null, unique, default)
        self.auto_now = auto_now

    def validate(self, value):
        """
        Validates the time value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated time value.

        Raises:
        - ValidationError: If the value is not a valid time.
        """
        value = super().validate(value)
        value = validate_time(value)
        return value


class ChoiceField(CharField):
    """
    Represents a choice field with predefined choices.

    Attributes:
    - choices (list): List of valid choices for the field.

    Methods:
    - validate(value): Validates that the value is one of the predefined choices.
    """

    def __init__(self, primary_key=False, null=True, unique=False, default=None, choices=None):
        super().__init__(max_length=max(len(choice) for choice in choices), primary_key=primary_key, null=null, unique=unique, default=default)
        self.choices = choices

    def validate(self, value):
        """
        Validates that the value is one of the predefined choices.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated choice value.

        Raises:
        - ValidationError: If the value is not one of the predefined choices.
        """
        value = Field().validate(value)
        value = validate_string(value, self.max_length)
        value = validate_choices(value, self.choices)
        return value


class ImageField(CharField):
    """
    Represents an image file field.

    Methods:
    - validate(value): Validates the image file path or URL.
    """

    def __init__(self, max_length=255, primary_key=False, null=True, unique=True, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        """
        Validates the image file path or URL.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated image file path or URL.

        Raises:
        - ValidationError: If the value is not a valid image file path or URL.
        """
        value = Field().validate(value)
        value = validate_string(value, self.max_length)
        return value


class FileField(CharField):
    """
    Represents a file field with allowed file types.

    Attributes:
    - allowed_types (list): List of allowed file types.

    Methods:
    - validate(value): Validates the file path or URL and checks file type.
    """

    def __init__(self, allowed_types, max_length=255, primary_key=False, null=True, unique=True, default=None):
        super().__init__(max_length, primary_key, null, unique, default)
        self.allowed_types = allowed_types

    def validate(self, value):
        """
        Validates the file path or URL and checks file type.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated file path or URL.

        Raises:
        - ValidationError: If the value is not a valid file path or URL or if the file type is not allowed.
        """
        value = Field().validate(value)
        value = validate_string(value, self.max_length)
        value = validate_file_type(value, self.allowed_types)
        return value


class URLField(CharField):
    """
    Represents a URL field.

    Methods:
    - validate(value): Validates the URL.
    """

    def __init__(self, max_length=255, primary_key=False, null=True, unique=True, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        """
        Validates the URL.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated URL.

        Raises:
        - ValidationError: If the value is not a valid URL.
        """
        value = Field().validate(value)
        value = validate_url(value)
        value = validate_string(value, self.max_length)
        return value


class ForeignKey(Field):
    """
    Represents a foreign key relationship to another model.

    Attributes:
    - to (Type): The model to which this field is related.

    Methods:
    - validate(value): Validates the foreign key value.
    """

    def __init__(self, to, primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)
        self.to = to

    def validate(self, value):
        """
        Validates the foreign key value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated foreign key value.

        Raises:
        - ValidationError: If the value is not a valid foreign key value.
        """
        value = super().validate(value)
        value = validate_integer(value)
        return value


class TextField(CharField):
    """
    Represents a text field for large text data.

    Methods:
    - validate(value): Validates the text value.
    """

    def __init__(self, max_length, primary_key=False, null=True, unique=False, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        """
        Validates the text value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated text value.

        Raises:
        - ValidationError: If the value does not meet text constraints.
        """
        value = super().validate(value)
        value = validate_string(value, self.max_length)
        return value


class PasswordField(CharField):
    """
    Represents a password field with hashing and salting.

    Attributes:
    - hash_name (str): The hashing algorithm used.
    - salt_size (int): The size of the salt used for hashing.
    - iterations (int): The number of hashing iterations.
    - salt (bytes): The salt used for hashing.

    Methods:
    - validate(value): Validates and hashes the password value.
    """

    def __init__(self, hash_name='sha256', salt_size=16, iterations=10e5, max_length=32, primary_key=False, null=True, unique=False, default=None):
        super().__init__(max_length, primary_key, null, unique, default)
        import os
        self.hash = hash_name
        self.salt_size = salt_size
        self.salt = os.urandom(salt_size)
        self.iterations = int(iterations)

    def validate(self, value):
        """
        Validates and hashes the password value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The hashed password.

        Raises:
        - ValidationError: If the value does not meet password constraints.
        """
        value = Field().validate(value)
        value = validate_password(value, self.hash, self.salt, self.max_length)
        return value


class EmailField(CharField):
    """
    Represents an email field.

    Methods:
    - validate(value): Validates the email address.
    """

    def __init__(self, max_length, primary_key=False, null=True, unique=False, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        """
        Validates the email address.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated email address.

        Raises:
        - ValidationError: If the value is not a valid email address.
        """
        value = Field().validate(value)
        value = validate_string(value, self.max_length)
        value = validate_email(value)
        return value


class ManyToManyField(Field):
    """
    Represents a many-to-many relationship to another model.

    Attributes:
    - to (Type): The model to which this field is related.
    - related_name (str): The name of the reverse relationship.

    Methods:
    - validate(value): Validates the many-to-many relationship value.
    """

    def __init__(self, to, related_name, null=True):
        super().__init__(null)
        self.to = to
        self.related_name = related_name

    def validate(self, value):
        """
        Validates the many-to-many relationship value.

        Args:
        - value: The value to be validated.

        Returns:
        - value: The validated many-to-many relationship value.

        Raises:
        - ValidationError: If the value is not valid for the many-to-many relationship.
        """
        value = super().validate(value)
        value = validate_integer(value)
        return value
