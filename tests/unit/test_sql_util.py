import pytest
from datetime import datetime

import os 
import sys

path = os.path.dirname(os.path.abspath('.'))
for root, dirs, files in os.walk(path):
    for _dir in dirs:
        sys.path.append(_dir)


from spiderweb_orm.models import Model
from spiderweb_orm import fields
from spiderweb_orm.sql_utils import SQLTypeGenerator, TableSQL
from spiderweb_orm.mysql.connection import MysqlConnection
from spiderweb_orm.sqlite.sqlite_connection import SQLIteConnection

class DummyModel(Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120,unique=True)
    age = fields.IntegerField()
    email =  fields.EmailField(max_length=120,unique=True)
    password = fields.PasswordField()
    created_at = fields.DateTimeField(auto_now=True)
    updated_at = fields.DateTimeField(auto_now=True)

    def create_table(self):
        sql = TableSQL().create_table_sql(self)
        return sql

    def save(self):
        query,values =  TableSQL().insert_data_sql(self)
        return query,values
   
@pytest.fixture
def type_generator():
    generator = SQLTypeGenerator()
    return generator

def test_char_field(type_generator):
    field = fields.CharField(max_length=120)
    assert type_generator.get_sql_type(field) == 'VARCHAR(120)'


def test_integer_field(type_generator):
    field = fields.IntegerField()
    assert type_generator.get_sql_type(field) == 'INTEGER'

def test_date_field(type_generator):
    field = fields.DateField()
    assert type_generator.get_sql_type(field) == 'DATE'

def test_datetime_field(type_generator):
    field = fields.DateTimeField()
    assert type_generator.get_sql_type(field) == 'DATETIME'

def test_float_field(type_generator):
    field = fields.FloatField()
    assert type_generator.get_sql_type(field) == 'FLOAT'

def test_decimal_field(type_generator):
    field = fields.DecimalField(max_digits=12,decimal_places=2)
    assert type_generator.get_sql_type(field) == 'DECIMAL(12, 2)'

def test_text_field(type_generator):
    field = fields.TextField(max_length=120)
    assert type_generator.get_sql_type(field) == 'TEXT(120)'

def test_time_field(type_generator):
    field = fields.TimeField()
    assert type_generator.get_sql_type(field) == 'TIME'

def test_boolean_field(type_generator):
    field = fields.BooleanField()
    assert type_generator.get_sql_type(field) == 'BOOLEAN'

def test_choice_field(type_generator):
    field = fields.ChoiceField(choices=['test'])
    assert type_generator.get_sql_type(field) == 'VARCHAR(4)'

def test_foreign_key(type_generator):
    field = fields.ForeignKey(to= DummyModel)
    assert type_generator.get_sql_type(field) == 'INTEGER REFERENCES dummymodel(id)'

def test_email_field(type_generator):
    field =  fields.EmailField(max_length=120)
    assert type_generator.get_sql_type(field) == 'VARCHAR(120)'

def test_image_field(type_generator):
    field =  fields.ImageField()
    assert type_generator.get_sql_type(field) == 'VARCHAR(255)'

def test_file_field(type_generator):
    field =  fields.FileField(allowed_types=None)
    assert type_generator.get_sql_type(field) == 'VARCHAR(255)'

def test_url_field(type_generator):
    field =  fields.URLField()
    assert type_generator.get_sql_type(field) == 'VARCHAR(255)'

def test_password_field(type_generator):
    field =  fields.PasswordField(max_length=120)
    assert type_generator.get_sql_type(field) == 'VARCHAR(120)'

def test_unknow_field(type_generator):
    class UnknowField:
        pass
    
    field = UnknowField()
    with pytest.raises(TypeError):
        type_generator.get_sql_type(field)


def test_mysql_create_table():
    model = DummyModel()
    model._meta['rdbms'] = MysqlConnection(host='localhost',user='root',password='root')  
    sql = model.create_table()
    expected_sql = (
        'CREATE TABLE IF NOT EXISTS dummymodel ('
        'id INTEGER PRIMARY KEY AUTO_INCREMENT,'
        'name VARCHAR(120) UNIQUE,'
        'age INTEGER,'
        'email VARCHAR(120) UNIQUE,'
        'password VARCHAR(32),'
        'created_at DATETIME,'
        'updated_at DATETIME);'
    )

    assert sql == expected_sql

def test_sqlite_create_table():
    model = DummyModel()   
    model._meta['rdbms'] = SQLIteConnection()
    sql = model.create_table()
    expected_sql = (
        'CREATE TABLE IF NOT EXISTS dummymodel ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'name VARCHAR(120) UNIQUE,'
        'age INTEGER,'
        'email VARCHAR(120) UNIQUE,'
        'password VARCHAR(32),'
        'created_at DATETIME,'
        'updated_at DATETIME);'
    )

    assert sql == expected_sql


def test_mysql_insert_data():
    instance = DummyModel(
        name = 'Simon Dev',
        age = 21,
        email = 'simon@gmail.com',
        password = '12354'
    )
    instance._meta['rdbms'] =  MysqlConnection(host='localhost',user='root',password='root')
    sql,dtime = instance.save(),datetime.now()
    query, values = sql

    expected_query = (
        'INSERT INTO dummymodel (name,age,email,password,created_at,updated_at) '
        'VALUES (%s,%s,%s,%s,%s,%s);'
    )
    from hashlib import sha256
    expected_values = [
        'Simon Dev',
        21,
        'simon@gmail.com',
        sha256(b'12354').digest(),
        dtime.__str__(),        
        dtime.__str__(),
        ]
    assert values == expected_values
    assert query == expected_query

def test_sqlite_insert_data():
    instance = DummyModel(
        name = 'Simon Dev',
        age = 21,
        email = 'simon@gmail.com',
        password = '12354'
    )
    instance._meta['rdbms'] =  SQLIteConnection()
    sql,dtime = instance.save(),datetime.now()
    query, values = sql

    expected_query = (
        'INSERT INTO dummymodel (name,age,email,password,created_at,updated_at) '
        'VALUES (?,?,?,?,?,?);'
    )
    from hashlib import sha256
    expected_values = [
        'Simon Dev',
        21,
        'simon@gmail.com',
        sha256(b'12354').digest(),
        dtime.__str__(),        
        dtime.__str__(),
        ]
    assert values == expected_values
    assert query == expected_query