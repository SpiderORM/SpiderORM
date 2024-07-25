from decimal import Decimal
from datetime import date,datetime,time

from spiderweb_orm.validators.exceptions import ValidationError
from spiderweb_orm.validators._re import verify_email_pattern,verify_url_pattern


def validate_required(value):
    if value is None or value == '':
        raise ValidationError('This field is required.')
    
def validate_null(value):
    if value is not None and value == '':
        raise ValidationError('This field can´t be null.')

def validate_string(value,max_length=None):    
    if not isinstance(value,str):
        raise ValidationError(f" Value must be a string: {value}.")
    if max_length and len(value) > max_length:
        raise ValidationError(f"Value exceeds maximun length of {max_length}.")
    
def validate_integer(value):
    if not isinstance(value, int):
        raise ValidationError(f"Value must be an integer: {value}.")

def validate_float(value):
    if not isinstance(value,float):
        raise ValidationError(f"Value must be a float: {value}.")

def validate_decimal(value):  
    
    if not isinstance(value, str):
        value = Decimal(value)
    if not isinstance(value,Decimal):
        raise ValidationError(f"Value must be a decimal.")       
            
def validate_boolean(value):
    if not isinstance(value,bool):
        raise ValidationError(f"Value must be a boolean: {value}.")
    
def validate_date(value):
    if not isinstance(value,date):
        raise ValidationError(f"Value must be a date: {value}.")
    
def validate_datetime(value):
    if not isinstance(value,datetime):
        raise ValidationError(f"Value must be a datetime: {value}.")

def validate_time(value):
    if not isinstance(value,time):
        raise ValidationError(f"Value must be a time: {value}.")

def validate_choices(value,choices):
    if value not in choices:
        raise ValidationError(f"Value must be one of {choices}.")

def validate_url(value):
    value = verify_url_pattern(value)
    if not value:
        raise ValidationError(f"Value must be a url.")
   
    
def validate_file_type(value,allowed_types):
    if not any(value.endswith(allowed_type) for allowed_type in allowed_types):
        raise ValidationError(f"Value must be one of {allowed_types}.")
    
def validate_default(value,default):
    return value if value is not None else default

def validate_email(value):
    value = verify_email_pattern(value)
    if not value:
        raise ValidationError(f"Value don't match with the email pattern.")
    