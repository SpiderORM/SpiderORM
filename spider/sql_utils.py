from spider.fields import *
from spider.mysql.connection import MysqlConnection
from datetime import datetime

class SQLTypeGenerator:
    """
    A class for generating SQL data types based on field types.
    """

    @staticmethod
    def get_sql_type(field):
        """
        Generate SQL data type for a given field.

        Args:
        - field (Field): The field for which to generate the SQL type.

        Returns:
        - str: The SQL data type string.

        Raises:
        - TypeError: If the field type is unknown.
        """
        field_type_map = {
            'CharField': lambda field: f"VARCHAR({field.max_length})",
            'IntegerField': lambda field: "INTEGER",
            'DecimalField': lambda field: f"DECIMAL({field.max_digits},{field.decimal_places})",
            'FloatField': lambda field: "FLOAT",
            'BooleanField': lambda field: "BOOLEAN",
            'DateField': lambda field: "DATE",
            'DateTimeField': lambda field: "DATETIME",
            'ChoiceField': lambda field: f"VARCHAR({field.max_length})",
            'ImageField': lambda field: "VARCHAR(255)",
            'FileField': lambda field: "VARCHAR(255)",
            'URLField': lambda field: "VARCHAR(255)",
            'ForeignKey': lambda field: f"INTEGER REFERENCES {field.to.__name__.lower()}(id)",
            'TextField': lambda field: f"TEXT({field.max_length})",
            'EmailField': lambda field: f"VARCHAR({field.max_length})",
            'PasswordField': lambda field: f"VARCHAR({field.max_length})",
            'TimeField': lambda field: "TIME",
        }

        field_class_name = field.__class__.__name__
        if field_class_name in field_type_map:
            return field_type_map[field_class_name](field)
        else:
            raise TypeError(f"Unknown field type: {type(field)}")

class TableSQL:
    """
    A class for generating SQL statements for table operations.
    """

    @staticmethod
    def create_table_sql(cls):
        """
        Generate SQL statement to create a table based on class definition.

        Args:
        - cls (Model): The model class that defines the table schema.

        Returns:
        - tuple: A tuple containing the CREATE TABLE SQL statement and an optional SQL statement 
          for password storage.
        """
        rdbms = cls._meta.get('rdbms')
        fields_definitions = []
        sql_safely_password_store_table = None
        auto_increment = ' AUTO_INCREMENT' if isinstance(rdbms, MysqlConnection) else ' AUTOINCREMENT'

        for field_name, field in cls._fields.items():
            if isinstance(field, PasswordField):
                field_def = f"{field_name}ID {SQLTypeGenerator.get_sql_type(field)}"
            else:
                field_def = f"{field_name} {SQLTypeGenerator.get_sql_type(field)}"
                
            if isinstance(field, PasswordField):
                sql_safely_password_store_table = f'CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, hash VARCHAR({field.max_length}) NOT NULL, salt VARCHAR({field.salt_size}) NOT NULL);'
            if field.primary_key:
                field_def += ' PRIMARY KEY'
            if getattr(field, 'auto_increment', False):
                field_def += auto_increment
            if not field.null:
                field_def += ' NOT NULL'
            if field.unique:
                field_def += ' UNIQUE'
            if field.default:
                field_def += f" DEFAULT {repr(field.default)}"

            fields_definitions.append(field_def)
        fields_sql = ",".join(fields_definitions)
        return f"CREATE TABLE IF NOT EXISTS {cls.__class__.__name__.lower()} ({fields_sql});", sql_safely_password_store_table

    @staticmethod
    def insert_data_sql(cls):
        """
        Generate SQL statement to insert data into a table based on class instance data.

        Args:
        - cls (Model): The model class that defines the table schema.

        Returns:
        - tuple: A tuple containing the INSERT SQL statement and a list of values.
        """
        value = None
        fields = []
        values = []
        rdbms = cls._meta.get('rdbms')
        _format_str = '%s' if isinstance(rdbms, MysqlConnection) else '?'
        has_password_field = False

        for field, field_class in cls._fields.items():
            if hasattr(field_class, 'auto_increment'):
                if not field_class.auto_increment:
                    fields.append(field)
                    value = getattr(cls, field)
            else:
                if isinstance(field_class, PasswordField):
                    fields.append(f'{field}ID')
                    has_password_field = True
                else:
                    fields.append(field)
                value = getattr(cls, field)

            if field_class.default is not None:
                if value == field_class:
                    value = value.default
                else:
                    value = value

            if isinstance(field_class, (DateField, DateTimeField)):
                if field_class.auto_now and not value or value == field_class:
                    _date = datetime.now().date()
                    _datetime = datetime.now()
                    value = _date.__str__() if isinstance(field_class, DateField) else _datetime.__str__()
                else:
                    value = value
            if isinstance(field_class, TimeField):
                if field_class.auto_now and not value or value == field_class:
                    value = datetime.now().time()
                else:
                    value = value.__str__()
            if isinstance(field_class, DecimalField):
                value = f"{value:.{field_class.decimal_places}f}"
            if value is not None:
                values.append(value)

        placeholders = ",".join([_format_str for _ in fields])
        columns = ",".join(fields)
        normal_insert = f"INSERT INTO {cls.__class__.__name__.lower()} ({columns}) VALUES ({placeholders});", values
        return normal_insert, has_password_field

    @staticmethod
    def filter_data_sql(cls, kwargs):
        """
        Generate SQL statement to filter data based on provided criteria.

        Args:
        - cls (Model): The model class that defines the table schema.
        - kwargs (dict): Dictionary of filter criteria.

        Returns:
        - tuple: A tuple containing the SELECT SQL statement and a list of values.
        """
        kwargs__lt = {}  # less than
        kwargs__lte = {}  # less than or equal to
        kwargs__gt = {}  # greater than
        kwargs__gte = {}  # greater than or equal to
        kwargs__eq = {}  # equal to
        kwargs__bt = {}  # between
        params = []
        values = []
        _format_str = '%s' if isinstance(cls._meta.get('rdbms'), MysqlConnection) else '?'

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

        if kwargs__eq:
            for eq_param in [f"{key} = {_format_str}" for key in kwargs__eq.keys()]:
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

        query = f"SELECT * FROM {cls.__class__.__name__.lower()} WHERE " + " AND ".join(params)

        return query, values

    @staticmethod
    def select_all_sql(cls):
        """
        Generate SQL statement to select all data from the table.

        Args:
        - cls (Model): The model class that defines the table schema.

        Returns:
        - str: The SELECT SQL statement.
        """
        return f"SELECT * FROM {cls.__class__.__name__.lower()};"

    @staticmethod
    def delete_data_sql(cls, id):
        """
        Generate SQL statement to delete data from the table based on ID.

        Args:
        - cls (Model): The model class that defines the table schema.
        - id (int): The ID of the record to delete.

        Returns:
        - tuple: A tuple containing the DELETE SQL statement and a list with the ID value.
        """
        _format_str = '%s' if isinstance(cls._meta.get('rdbms'), MysqlConnection) else '?'
        return f"DELETE FROM {cls.__class__.__name__.lower()} WHERE id = {_format_str};", [id]

    
    def update_data_sql(self,cls,kwargs):    
        params:list = []
        values:list = []     
        _format_str = '%s' if isinstance(cls._meta.get('rdbms'),MysqlConnection) else '?'
        
        field_to_update = [field for field in kwargs.keys() if self.get_field_type(field,cls)][0]        
        value_updated = [value for value in kwargs.values()][0]

        kwargs.pop(field_to_update) 

        cleaned_data = self.clean_data(cls,kwargs)        
        for key, value in cleaned_data.items():        
            params.append(f'{key} = {_format_str} ')
            values.append(value)
           
           

        query = f"UPDATE {cls.__class__.__name__.lower()} SET {field_to_update} = '{value_updated}' WHERE " + "AND ".join(params)        
        
        return query,values

    
    def clean_data(self,cls,kwargs):
        cleaned_data = {}
        for key, value in kwargs.items():
            field_type = self.get_field_type(key,cls)

            if isinstance(field_type,DecimalField):  
                validated_value = field_type.validate(value)
                cleaned_data[key] = validated_value
            else:
                cleaned_data[key] = value                                
        return cleaned_data

    def get_field_type(self,field,cls):
        try:
            field_type = cls._fields[field]
            return field_type
        except KeyError:
            raise KeyError(f"{field} is no a valid field to {cls.__class__.__name__}.")
