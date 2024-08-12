Field Types Module
==================

This module handles various field types used for database models,
including validation and sanitization of different types of data.

Classes
--------

.. class:: Field
    Base class for all field types.

    Attributes:
    - **primary_key** (bool): Indicates if this field is a primary key.
    - **null** (bool): Indicates if this field can be null.
    - **default**: Default value for the field if no value is provided.
    - **unique** (bool): Indicates if this field must have unique values.

.. class:: CharField(Field)
    Represents a string field with a maximum length.

    Attributes:
    - **max_length** (int): Maximum length of the string.

.. class:: IntegerField(Field)
    Represents an integer field, optionally with auto-increment.

    Attributes:
    - **auto_increment** (bool): Indicates if the field should auto-increment.

.. class:: DecimalField(Field)
    Represents a decimal field with precision and scale.

    Attributes:
    - **max_digits** (int): Total number of digits.
    - **decimal_places** (int): Number of decimal places.

.. class:: FloatField(Field)
    Represents a floating-point number field.

.. class:: BooleanField(Field)
    Represents a boolean field.

.. class:: DateField(Field)
    Represents a date field.

    Attributes:
    - **auto_now** (bool): Indicates if the field should auto-update to the current date.

.. class:: DateTimeField(Field)
    Represents a datetime field.

    Attributes:
    - **auto_now** (bool): Indicates if the field should auto-update to the current datetime.

.. class:: TimeField(Field)
    Represents a time field.

    Attributes:
    - **auto_now** (bool): Indicates if the field should auto-update to the current time.

.. class:: ChoiceField(CharField)
    Represents a choice field with predefined choices.

    Attributes:
    - **choices** (list): List of valid choices for the field.

.. class:: ImageField(CharField)
    Represents an image file field.

.. class:: FileField(CharField)
    Represents a file field with allowed file types.

    Attributes:
    - **allowed_types** (list): List of allowed file types.

.. class:: URLField(CharField)
    Represents a URL field.

.. class:: ForeignKey(Field)
    Represents a foreign key relationship to another model.

    Attributes:
    - **to** (Type): The model to which this field is related.

.. class:: TextField(CharField)
    Represents a text field for large text data.

.. class:: PasswordField(CharField)
    Represents a password field with hashing and salting.

    Attributes:
    - **hash_name** (str): The hashing algorithm used.
    - **salt_size** (int): The size of the salt used for hashing.
    - **iterations** (int): The number of hashing iterations.
    - **salt** (bytes): The salt used for hashing.

    Advantages:
    - **Enhanced Security**: By hashing and salting passwords, PasswordField provides an additional layer of security, protecting sensitive user data from potential breaches.
    - **Password Storage**: Passwords are stored in a hashed format, making it much harder for unauthorized users to retrieve or compromise the actual password values.
    - **Flexibility in Hashing Algorithms**: Supports different hashing algorithms through the `hash_name` attribute, allowing adaptation to various security standards and practices.
    - **Salting and Iterations**: Uses salt and multiple hashing iterations to defend against rainbow table attacks and brute-force attacks, enhancing overall security.
    - **Integration with a Separate Table**: When used in a model, PasswordField can trigger the creation of a dedicated table for storing encrypted passwords. This helps in organizing and securing password data separately from other user information.


.. class:: EmailField(CharField)
    Represents an email field.

.. class:: ManyToManyField(Field)
    Represents a many-to-many relationship to another model.

    Attributes:
    - **to** (Type): The model to which this field is related.
    - **related_name** (str): The name of the reverse relationship.
