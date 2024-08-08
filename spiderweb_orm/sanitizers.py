import re
from decimal import Decimal
from datetime import datetime
from html import escape
from spiderweb_orm.validators._re import verify_url_pattern

def sanitize_string(value):
    sanitized_value = re.sub(r'[^\W\S]','',value)
    return escape(sanitized_value)

def sanitize_integer(value):
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid integer value: {value}.")

def sanitize_float(value):
    try: 
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid float value: {value}.")

def sanitize_decimal(value):
    try:    
        return Decimal(value)
    except ValueError:
        raise ValueError(f"Invalid decimal value: {value}.")

def sanitize_boolean(value):
    if isinstance(value,bool):
        return value
    if value.lower() in ['true','1','yes']:
        return True
    elif value.lower() in ['false','0','no','not']:
        return False        
    else:
        raise ValueError(f"invalid boolean value: {value}.")

def sanitize_date(value):
    try:
        return datetime.strptime(value,"%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date value: {value}.")

def sanitize_datetime(value):
    try:
        return datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"Invalid datetime value: {value}.")

def sanitize_time(value):
    try:
        return datetime.strptime(value,"%H:%M:%S").time()
    except ValueError:
        raise ValueError(f"Invalid time value: {value}.")

def sanitize_choice(value,choices):
    if value in choices:
        return value
    else:
        raise ValueError(f"Invalid choice value: {value}.")

def sanitize_url(value):
    if verify_url_pattern(value):
        return value
    else:
        raise ValueError(f"Invalid URL value: {value}.")

def sanitize_file(value,allowed_types):
    if value.split('.')[-1] in allowed_types:
        return value    
    else: 
        raise ValueError(f"Invalid file type: {value}.")

def sanitize_image(value):
    if value.split('.')[-1] in ['png','jpg','gif']:
        return value
    else:
        raise ValueError(f"Invalid image value: {value}.")