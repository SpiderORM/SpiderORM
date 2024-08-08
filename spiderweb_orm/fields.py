"""

    This module handle the diferents fields type.

"""


from spiderweb_orm.validators.fields_validations import (
    validate_boolean,validate_choices,
    validate_date,validate_datetime,
    validate_decimal,validate_default,
    validate_file_type,validate_float,
    validate_integer,validate_null,
    validate_string,validate_url,
    validate_email,validate_time,
    validate_password
)


class Field:
    def __init__(self,primary_key=False,null=True,unique=False,default=None):
        self.primary_key = primary_key
        self.null = null
        self.default = default
        self.unique = unique

    def validate(self,value):
        if self.null:
            validate_null(value)
        if self.default:
            validate_default(value,self.default)
        return value

class CharField(Field):
    def __init__(self, max_length,primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)
        self.max_length = max_length        

    def validate(self, value):
        value = super().validate(value)
        value = validate_string(value,self.max_length)
        return value

class IntegerField(Field):
    def __init__(self, primary_key=False, null=True, unique=False, default=None,auto_increment=False):
        super().__init__(primary_key, null, unique, default)
        self.auto_increment = auto_increment

    def validate(self, value):
        value = super().validate(value)
        value = validate_integer(value)
        return value
    
class DecimalField(Field):
    def __init__(self, max_digits,decimal_places,primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)
        self.max_digits = max_digits
        self.decimal_places = decimal_places
            
    def validate(self, value):
        value = super().validate(value)
        value = validate_decimal(value)
        return value

class FloatField(Field):
    def __init__(self, primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)

    def validate(self, value):        
        value = super().validate(value)
        value = validate_float(value)
        return value

class BooleanField(Field):
    def __init__(self, primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)

    def validate(self, value):
        value =  super().validate(value)
        value = validate_boolean(value)
        return value

class DateField(Field):
    def __init__(self, primary_key=False, null=True, unique=False, default=None,auto_now=False):
        super().__init__(primary_key, null, unique, default)
        self.auto_now = auto_now

    def validate(self, value):        
        value =  super().validate(value)
        value = validate_date(value)
        return value
                
class DateTimeField(Field):
    def __init__(self, primary_key=False, null=True, unique=False, default=None,auto_now =False):
        super().__init__(primary_key, null, unique, default)
        self.auto_now = auto_now

    def validate(self, value):
        value = super().validate(value)
        value = validate_datetime(value)
        return value

class TimeField(Field):
    def __init__(self, primary_key=False, null=True, unique=False, default=None,auto_now=False):
        super().__init__(primary_key, null, unique, default)
        self.auto_now = auto_now

    def validate(self, value):
        value = super().validate(value)
        value = validate_time(value)
        return value

class ChoiceField(CharField):    
    def __init__(self,primary_key=False, null=True, unique=False, default=None,choices=None):
        super().__init__(max_length=max(len(choice) for choice in choices), primary_key=primary_key, null=null, unique=unique, default=default)
        self.choices = choices
    
    def validate(self, value):        
        value = Field().validate(value)
        value = validate_string(value,self.max_length)
        value = validate_choices(value,self.choices)
        return value

class ImageField(CharField):
    def __init__(self, max_length=255, primary_key=False, null=True, unique=True, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        value = Field().validate(value)
        value = validate_string(value,self.max_length)        
        return value
    
class FileField(CharField):
    def __init__(self, allowed_types,max_length=255, primary_key=False, null=True, unique=True, default=None):
        super().__init__(max_length, primary_key, null, unique, default)
        self.allowed_types = allowed_types

    def validate(self, value):
        value = Field().validate(value)
        value = validate_string(value,self.max_length)                
        value = validate_file_type(value,self.allowed_types)
        return value
    
class URLField(CharField):
    def __init__(self, max_length=255, primary_key=False, null=True, unique=True, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        value = Field().validate(value)
        value = validate_url(value)
        value = validate_string(value,self.max_length)        
        return value

class ForeignKey(Field):
    def __init__(self, to,primary_key=False, null=True, unique=False, default=None):
        super().__init__(primary_key, null, unique, default)
        self.to =to

    def validate(self, value):
        value =  super().validate(value)
        value = validate_integer(value)
        return value 
    
class TextField(CharField):
    def __init__(self, max_length, primary_key=False, null=True, unique=False, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        value =  super().validate(value)
        value = validate_string(value,self.max_length)
        return value

class PasswordField(CharField):
    def __init__(self,hash_name='sha256',salt_size=16,iterations=10e5, max_length=32, primary_key=False, null=True, unique=False, default=None):
        super().__init__(max_length, primary_key, null, unique, default)
        import os 
        self.hash = hash_name
        self.salt_size = salt_size
        self.salt = os.urandom(salt_size)
        self.iterations = int(iterations)

    def validate(self, value):
        value = Field().validate(value)
        value = validate_password(value,self.hash,self.salt,self.max_length)
        return value
    
class EmailField(CharField):
    def __init__(self, max_length, primary_key=False, null=True, unique=False, default=None):
        super().__init__(max_length, primary_key, null, unique, default)

    def validate(self, value):
        value = Field().validate(value)        
        value = validate_string(value,self.max_length)
        value = validate_email(value)
        return value


class ManyToManyField(Field):
    def __init__(self,to,related_name,null=True):        
        super().__init__(null)
        self.to = to
        self.relate_name = related_name

    def validate(self, value):
        value =  super().validate(value)
        value = validate_integer(value)
        return value 