from spiderweb_orm.fields import Field
from spiderweb_orm.sql_utils import TableSQL
from spiderweb_orm.validators.exceptions import ValidationError
from spiderweb_orm.sqlite3.sqlite_connection import SQLIteConnection

class ModelMeta(type):
    def __new__(cls,name,bases,attrs):
        fields = {key: value for key, value in attrs.items() if isinstance(value,Field)}
        new_class = super().__new__(cls,name,bases,attrs)
        new_class._fields = fields
        return new_class
    
class Model(metaclass=ModelMeta):

    def __init__(self,**kwargs) -> None:
        for key, value in kwargs.items():
            if key in self._fields:
                setattr(self,key,self._fields[key].validate(value))
            else:
                raise AttributeError(f"{key} is not a valid field for {self.__class__.__name__}")
        
    @staticmethod
    def create_table(cls):
        sql = TableSQL.create_table_sql(cls)        
        with SQLIteConnection() as conn:
            conn.execute(sql)
                
    def save(self):
        sql,values = TableSQL.insert_data_sql(self)        
        with SQLIteConnection() as conn:            
            conn.execute(sql,values)