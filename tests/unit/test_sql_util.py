import pytest
from datetime import datetime

import os 
import sys

path = os.path.dirname(os.path.abspath('.'))
for root, dirs, files in os.walk(path):
    for _dir in dirs:
        sys.path.append(_dir)


from spider.models import Model
from spider import fields
from spider.sql_utils import SQLTypeGenerator, TableSQL
from spider.mysql.connection import MysqlConnection
from spider.sqlite.sqlite_connection import SQLIteConnection

class DummyModel(Model):
    """
    Representa um modelo dummy com vários campos, incluindo id, name, age, email, password e timestamps.
    """

    id = fields.IntegerField(primary_key=True, auto_increment=True)
    name = fields.CharField(max_length=120, unique=True)
    age = fields.IntegerField()
    email = fields.EmailField(max_length=120, unique=True)
    password = fields.PasswordField()
    created_at = fields.DateTimeField(auto_now=True)
    updated_at = fields.DateTimeField(auto_now=True)

    def create_table(self):
        """
        Gera a declaração SQL para criar a tabela para este modelo.

        Returns:
        - str: A declaração SQL para criar a tabela.
        """
        sql = TableSQL().create_table_sql(self)[0]
        return sql

    def create_password_table(self):
        """
        Gera a declaração SQL para criar a tabela de senhas.

        Returns:
        - str: A declaração SQL para criar a tabela de senhas.
        """
        sql = TableSQL().create_table_sql(self)[1]
        return sql

    def save(self):
        """
        Gera a declaração SQL e os valores para inserir dados na tabela.

        Returns:
        - tuple: Um tuplo contendo a declaração SQL de inserção e os valores a serem inseridos.
        """
        query, values = TableSQL().insert_data_sql(self)[0]
        return query, values

    def has_password_insert(self):
        """
        Verifica se a tabela de senhas foi inserida.

        Returns:
        - bool: True se a tabela de senhas foi inserida, caso contrário False.
        """
        result = TableSQL().insert_data_sql(self)[1]
        return result

    def filter(self, **kwargs):
        """
        Gera a declaração SQL para filtrar dados com base nos critérios fornecidos.

        Parameters:
        - kwargs: Critérios para filtrar os dados.

        Returns:
        - tuple: Um tuplo contendo a declaração SQL de seleção e os valores para a consulta.
        """
        sql = TableSQL().filter_data_sql(self, kwargs)
        return sql

    def all(self):
        """
        Gera a declaração SQL para selecionar todos os registros da tabela.

        Returns:
        - str: A declaração SQL para recuperar todos os registros.
        """
        sql = TableSQL().select_all_sql(self)
        return sql

    def delete(self, id):
        """
        Gera a declaração SQL para excluir um registro pelo seu ID.

        Parameters:
        - id (int): O ID do registro a ser excluído.

        Returns:
        - tuple: Um tuplo contendo a declaração SQL de exclusão e o valor do ID.
        """
        sql = TableSQL().delete_data_sql(self, id)
        return sql

@pytest.fixture
def type_generator():
    """
    Fixture para criar uma instância do SQLTypeGenerator.

    Returns:
    - SQLTypeGenerator: A instância do gerador de tipos.
    """
    generator = SQLTypeGenerator()
    return generator

def test_char_field(type_generator):
    """
    Testa a verificação do tipo SQL de um CharField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.CharField(max_length=120)
    assert type_generator.get_sql_type(field) == 'VARCHAR(120)'

def test_integer_field(type_generator):
    """
    Testa a verificação do tipo SQL de um IntegerField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.IntegerField()
    assert type_generator.get_sql_type(field) == 'INTEGER'

def test_date_field(type_generator):
    """
    Testa a verificação do tipo SQL de um DateField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.DateField()
    assert type_generator.get_sql_type(field) == 'DATE'

def test_datetime_field(type_generator):
    """
    Testa a verificação do tipo SQL de um DateTimeField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.DateTimeField()
    assert type_generator.get_sql_type(field) == 'DATETIME'

def test_float_field(type_generator):
    """
    Testa a verificação do tipo SQL de um FloatField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.FloatField()
    assert type_generator.get_sql_type(field) == 'FLOAT'

def test_decimal_field(type_generator):
    """
    Testa a verificação do tipo SQL de um DecimalField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.DecimalField(max_digits=12, decimal_places=2)
    assert type_generator.get_sql_type(field) == 'DECIMAL(12,2)'

def test_text_field(type_generator):
    """
    Testa a verificação do tipo SQL de um TextField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.TextField(max_length=120)
    assert type_generator.get_sql_type(field) == 'TEXT(120)'

def test_time_field(type_generator):
    """
    Testa a verificação do tipo SQL de um TimeField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.TimeField()
    assert type_generator.get_sql_type(field) == 'TIME'

def test_boolean_field(type_generator):
    """
    Testa a verificação do tipo SQL de um BooleanField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.BooleanField()
    assert type_generator.get_sql_type(field) == 'BOOLEAN'

def test_choice_field(type_generator):
    """
    Testa a verificação do tipo SQL de um ChoiceField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.ChoiceField(choices=['test'])
    assert type_generator.get_sql_type(field) == 'VARCHAR(4)'

def test_foreign_key(type_generator):
    """
    Testa a verificação do tipo SQL de um ForeignKey.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.ForeignKey(to=DummyModel)
    assert type_generator.get_sql_type(field) == 'INTEGER REFERENCES dummymodel(id)'

def test_email_field(type_generator):
    """
    Testa a verificação do tipo SQL de um EmailField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.EmailField(max_length=120)
    assert type_generator.get_sql_type(field) == 'VARCHAR(120)'

def test_image_field(type_generator):
    """
    Testa a verificação do tipo SQL de um ImageField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.ImageField()
    assert type_generator.get_sql_type(field) == 'VARCHAR(255)'

def test_file_field(type_generator):
    """
    Testa a verificação do tipo SQL de um FileField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.FileField(allowed_types=None)
    assert type_generator.get_sql_type(field) == 'VARCHAR(255)'

def test_url_field(type_generator):
    """
    Testa a verificação do tipo SQL de um URLField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.URLField()
    assert type_generator.get_sql_type(field) == 'VARCHAR(255)'

def test_password_field(type_generator):
    """
    Testa a verificação do tipo SQL de um PasswordField.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    field = fields.PasswordField(max_length=120)
    assert type_generator.get_sql_type(field) == 'VARCHAR(120)'

def test_unknown_field(type_generator):
    """
    Testa o comportamento quando um tipo de campo desconhecido é fornecido.

    Parameters:
    - type_generator (SQLTypeGenerator): A instância do gerador de tipos.
    """
    class UnknownField:
        pass
    
    field = UnknownField()
    with pytest.raises(TypeError):
        type_generator.get_sql_type(field)

def test_mysql_create_table():
    """
    Testa a geração das declarações SQL corretas para criar tabelas no MySQL.

    Verifica a criação tanto da tabela principal quanto da tabela de senhas.
    """
    model = DummyModel()
    model._meta['rdbms'] = MysqlConnection(host='localhost', user='root', password='root')
    sql = model.create_table()
    sql_password_table = model.create_password_table()

    expected_sql_password_table = (
        'CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, hash VARCHAR(32) NOT NULL, salt VARCHAR(16) NOT NULL);'
    )
    expected_sql = (
        'CREATE TABLE IF NOT EXISTS dummymodel ('
        'id INTEGER PRIMARY KEY AUTO_INCREMENT,'
        'name VARCHAR(120) UNIQUE,'
        'age INTEGER,'
        'email VARCHAR(120) UNIQUE,'
        'passwordID VARCHAR(32),'
        'created_at DATETIME,'
        'updated_at DATETIME);'
    )

    assert sql == expected_sql
    assert sql_password_table == expected_sql_password_table

def test_sqlite_create_table():
    """
    Testa a geração das declarações SQL corretas para criar tabelas no SQLite.

    Verifica a criação tanto da tabela principal quanto da tabela de senhas.
    """
    model = DummyModel()
    model._meta['rdbms'] = SQLIteConnection()
    sql = model.create_table()
    sql_password_table = model.create_password_table()

    expected_sql_password_table = (
        'CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, hash VARCHAR(32) NOT NULL, salt VARCHAR(16) NOT NULL);'
    )
    expected_sql = (
        'CREATE TABLE IF NOT EXISTS dummymodel ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'name VARCHAR(120) UNIQUE,'
        'age INTEGER,'
        'email VARCHAR(120) UNIQUE,'
        'passwordID VARCHAR(32),'
        'created_at DATETIME,'
        'updated_at DATETIME);'
    )

    assert sql == expected_sql
    assert sql_password_table == expected_sql_password_table

@pytest.mark.xfail
def test_mysql_insert_data(): 
    """
    Testa a geração da declaração SQL e valores para inserção de dados no MySQL.

    Verifica se a declaração SQL de inserção e os valores correspondem ao esperado e se a tabela de senhas foi inserida.
    """
    instance = DummyModel(
        name='Simon Dev',
        age=21,
        email='simon@gmail.com',
        password='12354'
    )
    instance._meta['rdbms'] = MysqlConnection(host='localhost', user='root', password='root')
    sql, dtime = instance.save(), datetime.now()
    query, values = sql
    has_password_insert = instance.has_password_insert()

    expected_query = (
        'INSERT INTO dummymodel (name,age,email,passwordID,created_at,updated_at) '
        'VALUES (%s,%s,%s,%s,%s,%s);'
    )
    
    expected_values = [
        'Simon Dev',
        21,
        'simon@gmail.com',
        '12354',
        dtime.__str__(),
        dtime.__str__(),
    ]
    assert values == expected_values
    assert query == expected_query
    assert has_password_insert == True

@pytest.mark.xfail
def test_sqlite_insert_data():
    """
    Testa a geração da declaração SQL e valores para inserção de dados no SQLite.

    Verifica se a declaração SQL de inserção e os valores correspondem ao esperado e se a tabela de senhas foi inserida.
    """
    instance = DummyModel(
        name='Simon Dev',
        age=21,
        email='simon@gmail.com',
        password='12354'
    )
    instance._meta['rdbms'] = SQLIteConnection()
    sql, dtime = instance.save(), datetime.now()
    query, values = sql
    has_password_insert = instance.has_password_insert()

    expected_query = (
        'INSERT INTO dummymodel (name,age,email,passwordID,created_at,updated_at) '
        'VALUES (?,?,?,?,?,?);'
    )
    expected_values = [
        'Simon Dev',
        21,
        'simon@gmail.com',
        '12354',
        dtime.__str__(),
        dtime.__str__(),
    ]
    assert values == expected_values
    assert query == expected_query
    assert has_password_insert == True

def test_mysql_filter_data():
    """
    Testa a geração da declaração SQL para filtrar dados no MySQL.

    Verifica se a declaração SQL de seleção e os valores correspondem ao esperado para os critérios fornecidos.
    """
    instance = DummyModel()
    instance._meta['rdbms'] = MysqlConnection(host='localhost', user='root', password='root')

    query, values = instance.filter(age__lt=30, email='simon@gmail.com')
    expected_query = 'SELECT * FROM dummymodel WHERE email = %s AND age < %s'
    expected_values = ['simon@gmail.com', 30]

    assert query == expected_query
    assert values == expected_values

def test_sqlite_filter_data():
    """
    Testa a geração da declaração SQL para filtrar dados no SQLite.

    Verifica se a declaração SQL de seleção e os valores correspondem ao esperado para os critérios fornecidos.
    """
    instance = DummyModel()
    instance._meta['rdbms'] = SQLIteConnection()

    query, values = instance.filter(age__lt=30, email='simon@gmail.com')
    expected_query = 'SELECT * FROM dummymodel WHERE email = ? AND age < ?'
    expected_values = ['simon@gmail.com', 30]

    assert query == expected_query
    assert values == expected_values

def test_mysql_select_all():
    """
    Testa a geração da declaração SQL para selecionar todos os registros no MySQL.

    Verifica se a declaração SQL de seleção corresponde ao esperado.
    """
    mysql_conn_instance = DummyModel()    
    mysql_conn_instance._meta['rdbms'] = MysqlConnection(host='localhost', user='root', password='root')    

    mysql_query = mysql_conn_instance.all()    
    mysql_expected_query = 'SELECT * FROM dummymodel;'    

    assert mysql_query == mysql_expected_query 

def test_sqlite_select_all():
    """
    Testa a geração da declaração SQL para selecionar todos os registros no SQLite.

    Verifica se a declaração SQL de seleção corresponde ao esperado.
    """
    sqlite_conn_instance = DummyModel()
    sqlite_conn_instance._meta['rdbms'] = SQLIteConnection()

    sqlite_query = sqlite_conn_instance.all()
    sqlite_expected_query = 'SELECT * FROM dummymodel;'
    
    assert sqlite_query == sqlite_expected_query

def test_mysql_delete_data():
    """
    Testa a geração da declaração SQL para excluir um registro pelo ID no MySQL.

    Verifica se a declaração SQL de exclusão e o valor do ID correspondem ao esperado.
    """
    mysql_conn_instance = DummyModel()   
    mysql_conn_instance._meta['rdbms'] = MysqlConnection(host='localhost', user='root', password='root')    

    mysql_query, mysql_values = mysql_conn_instance.delete(id=1)    
    mysql_expected_query = 'DELETE FROM dummymodel WHERE id = %s;'  

    expected_value = 1
    assert mysql_query == mysql_expected_query   
    assert mysql_values[0] == expected_value

def test_sqlite_delete_data():
    """
    Testa a geração da declaração SQL para excluir um registro pelo ID no SQLite.

    Verifica se a declaração SQL de exclusão e o valor do ID correspondem ao esperado.
    """
    sqlite_conn_instance = DummyModel()
    sqlite_conn_instance._meta['rdbms'] = SQLIteConnection()

    sqlite_query, sqlite_values = sqlite_conn_instance.delete(id=1)
    sqlite_expected_query = 'DELETE FROM dummymodel WHERE id = ?;'

    expected_value = 1
    assert sqlite_query == sqlite_expected_query
    assert sqlite_values[0] == expected_value
