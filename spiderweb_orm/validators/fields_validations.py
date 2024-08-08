from decimal import Decimal
from datetime import date,datetime,time

from spiderweb_orm.validators.exceptions import ValidationError
from spiderweb_orm.validators._re import verify_email_pattern,verify_url_pattern
from spiderweb_orm.sanitizers import *


def validate_required(value):
    if value is None or value == '':
        raise ValidationError('This field is required.')
    
def validate_null(value):
    if value is not None and value == '':
        raise ValidationError('This field can´t be null.')

def validate_string(value,max_length=None):    
    value =  sanitize_string(value)
    if not isinstance(value,str):
        raise ValidationError(f" Value must be a string: {value}.")
    if max_length and len(value) > max_length:
        raise ValidationError(f"Value exceeds maximun length of {max_length}.")
    return value    
    
def validate_integer(value):
    value =  sanitize_integer(value)
    if not isinstance(value, int):
        raise ValidationError(f"Value must be an integer: {value}.")
    return value

def validate_float(value):
    value =  sanitize_float(value)
    if not isinstance(value,float):
        raise ValidationError(f"Value must be a float: {value}.")    
    return value

def validate_decimal(value):     
    value =  sanitize_decimal(value)
    if not isinstance(value,Decimal):
        raise ValidationError(f"Value must be a decimal.") 
    return value     
            
def validate_boolean(value):
    if not isinstance(value,bool):
        raise ValidationError(f"Value must be a boolean: {value}.")
    value =  sanitize_boolean(value)
    return value
    
def validate_date(value):
    value =  sanitize_date(value)
    if not isinstance(value,date):
        raise ValidationError(f"Value must be a date: {value}.")
    return value        
    
def validate_datetime(value):
    value =  sanitize_datetime(value)
    if not isinstance(value,datetime):
        raise ValidationError(f"Value must be a datetime: {value}.")
    return value

def validate_time(value):
    value =  sanitize_time(value)
    if not isinstance(value,time):
        raise ValidationError(f"Value must be a time: {value}.")
    return value

def validate_choices(value,choices):
    value =  sanitize_string(value)
    if value not in choices:
        raise ValidationError(f"Value must be one of {choices}.")
    return value

def validate_url(value):
    value =  sanitize_url(value)    
    if not value:
        raise ValidationError(f"Value must be a url.")
    return value   
    
def validate_file_type(value,allowed_types):
    value =  sanitize_file(value)
    if not any(value.endswith(allowed_type) for allowed_type in allowed_types):
        raise ValidationError(f"Value must be one of {allowed_types}.")
    return value
    
def validate_default(value,default):
    return value if value is not None else default

def validate_email(value):    
    value =  sanitize_string(value)
    if not verify_email_pattern(value):
        raise ValidationError(f"Value don't match with the email pattern.") 
    return value

def validate_password(value,hash,salt,max_length):
    from hashlib import algorithms_available

    value =  sanitize_string(value)
    validate_choices(hash,choices=list(algorithms_available))
    validate_string(value,max_length)
    if not isinstance(salt,bytes):
        raise ValidationError(f"salt must be a bytes instance.")
    return value