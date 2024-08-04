"""

"""
from spiderweb_orm.fields import *
from spiderweb_orm.sqlite.sqlite_connection import SQLIteConnection
from spiderweb_orm.mysql.connection import MysqlConnection
from datetime import datetime
from hashlib import sha256,pbkdf2_hmac
import os

class SQLTypeGenerator:
    
    @staticmethod
    def get_sql_type(field):
        field_type_map = {
            'CharField':lambda field: f"VARCHAR({field.max_length})",
            'IntegerField':lambda field:f"INTEGER",
            'DecimalField':lambda field:f"DECIMAL{field.max_digits,field.decimal_places}",
            'FloatField':lambda field:f"FLOAT",
            'BooleanField':lambda field:f"BOOLEAN",
            'DateField':lambda field:f"DATE",
            'DateTimeField':lambda field:f"DATETIME",
            'ChoiceField':lambda field:f"VARCHAR({field.max_length})",
            'ImageField':lambda field:f"VARCHAR(255)",
            'FileField':lambda field:f"VARCHAR(255)",
            'URLField':lambda field:f"VARCHAR(255)",
            'ForeignKey':lambda field:f"INTEGER REFERENCES {field.to.__name__.lower()}(id)",
            'TextField':lambda field:f"TEXT",
            'EmailField':lambda field:f"VARCHAR({field.max_length})",
            'PasswordField':lambda field:f"VARCHAR({field.max_length})",
            'TimeField':lambda field:f"TIME",
        }

        field_class_name = field.__class__.__name__
        if field_class_name in field_type_map:
            return field_type_map[field_class_name](field)
        else:
            raise TypeError(f"Unknown field type: {type(field)}")


class TableSQL:

    @staticmethod
    def create_table_sql(cls):
        rdbms = cls._meta.get('rdbms')
        fields_definitions = []
        for field_name, field in cls._fields.items():
            field_def = f"{field_name} {SQLTypeGenerator.get_sql_type(field)}"
            if field.primary_key:
                field_def += ' PRIMARY KEY'
            if getattr(field,'auto_increment',False):
                if isinstance(rdbms,SQLIteConnection):
                    field_def += ' AUTOINCREMENT'
                elif isinstance(rdbms,MysqlConnection):
                    field_def += ' AUTO_INCREMENT'
            if not field.null:
                field_def += ' NOT NULL'
            if field.unique:                
                field_def += ' UNIQUE'
            if field.default:
                field_def += f" DEFAULT {repr(field.default)}"

            fields_definitions.append(field_def)
        fields_sql = ",".join(fields_definitions)
        return f"CREATE TABLE IF NOT EXISTS {cls.__class__.__name__.lower()} ({fields_sql});"
    
    @staticmethod
    def insert_data_sql(cls):
        value = None  
        fields = []                
        values = []
        rdbms = cls._meta.get('rdbms')
        _format_str = '%s' if isinstance(rdbms,MysqlConnection) else '?' 

        for field, field_class in cls._fields.items():   
                                
            if hasattr(field_class,'auto_increment'): 
                if not field_class.auto_increment:
                    fields.append(field)     
                    value = field_class.validate(getattr(cls,field))
            else:
                fields.append(field)
                value = getattr(cls,field)

            if field_class.default is not None:                                             
                if value == field_class:                     
                    value = field_class.validate(value.default)
                else:                    
                    value = field_class.validate(value)
            
            if isinstance(field_class,(DateField,DateTimeField)):
                if field_class.auto_now and not value or value == field_class:  
                    _date = datetime.now().date()
                    _datetime =datetime.now()
                    value = field_class.validate(_date).__str__() if isinstance(field_class,DateField) else field_class.validate(_datetime).__str__()
                else:
                    value = field_class.validate(value)
            if isinstance(field_class,TimeField):
                if field_class.auto_now and not value or value == field_class:
                    value = field_class.validate(datetime.now().time())
                else:
                    value = field_class.validate(value).__str__()
            if isinstance(field_class,(PasswordField)):

                # TODO: Store the salt in database

                salt = os.urandom(16)
                _hash = pbkdf2_hmac(hash_name='sha256',password=field_class.validate(value).encode(),salt=salt,iterations=100000)
                value = _hash.hex() 
                               
            if isinstance(field_class,DecimalField):
                value =  f"{field_class.validate(value):.{field_class.decimal_places}f}"            
            if value is not None:
                values.append(value)                    
                 
        placeholders = ",".join([f"{_format_str}" for _ in fields])
        columns = ",".join(fields)        
        return  f"INSERT INTO {cls.__class__.__name__.lower()} ({columns}) VALUES ({placeholders});",values

    @staticmethod
    def filter_data_sql(cls,kwargs):
        kwargs__lt:dict = {} # less than 
        kwargs__lte:dict = {} # less than or equal to
        kwargs__gt:dict = {} # great than 
        kwargs__gte:dict = {} # great than or equal to
        kwargs__eq:dict = {} # equal to
        kwargs__bt:dict = {} # between
        params:list = []
        values:list = []
        _format_str = '%s' if isinstance(cls._meta.get('rdbms'),MysqlConnection) else '?'

        for key, value in kwargs.items():                                   
            if key.endswith('__lt'):               
                kwargs__lt[key] = value            
            elif key.endswith('__gt'):
                kwargs__gt[key] = value
            elif key.endswith('__lte'):
                kwargs__lte[key] = value
            elif key.endswith('__gte'):
                kwargs__gte[key] = value
            elif key.endswith('__bt'):
                kwargs__bt[key] = value
            else:
                kwargs__eq[key] = value

        query =  f"SELECT * FROM {cls.__class__.__name__.lower()} WHERE "         
        
        if kwargs__eq:
            for eq_param in [f"{key} = {_format_str} " for key in kwargs__eq.keys()]:
                params.append(eq_param)
            for value in kwargs__eq.values():
                values.append(value)
        if kwargs__lt: 
            for lt_param in [f"{key.removesuffix('__lt')} < {_format_str}" for key in kwargs__lt.keys()]:
                params.append(lt_param)           
            for value in kwargs__lt.values():               
               values.append(value)
        if kwargs__lte: 
            for lte_param in [f"{key.removesuffix('__lte')} <= {_format_str}" for key in kwargs__lte.keys()]:
                params.append(lte_param)           
            for value in kwargs__lte.values():               
               values.append(value)
        if kwargs__gt:             
            for gt_params in [f"{key.removesuffix('__gt')} > {_format_str}" for key in kwargs__gt.keys()]:
                params.append(gt_params)                      
            for value in kwargs__gt.values():
               values.append(value)
        if kwargs__gte:             
            for gte_params in [f"{key.removesuffix('__gte')} >= {_format_str}" for key in kwargs__gte.keys()]:
                params.append(gte_params)                      
            for value in kwargs__gte.values():
               values.append(value)
        if kwargs__bt:
            for bt_params in [f"{key.removesuffix('__bt')} BETWEEN {_format_str} AND {_format_str}" for key in kwargs__bt.keys()]:
                params.append(bt_params)
            for value in kwargs__bt.values():
                values.append(value[0])
                values.append(value[1])
        
        query += 'AND '.join(params)

        return query,values
    
    @staticmethod
    def select_all_sql(cls):
        return f"SELECT * FROM {cls.__class__.__name__.lower()};"
    
    @staticmethod
    def delete_data_sql(cls,id):
        _format_str = '%s' if isinstance(cls._meta.get('rdbms'),MysqlConnection) else '?'
        param = str(id)
        query = f"DELETE FROM {cls.__class__.__name__.lower()} WHERE id = {_format_str};"
        return query,param