from spiderweb_orm.fields import Field
from spiderweb_orm.sql_utils import TableSQL
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
       
    def create_table(self):
        sql = TableSQL.create_table_sql(self)        
        with SQLIteConnection() as conn:
            conn.execute(sql)
            print('Table created successfully.')
    
    
    def filter(self,**kwargs):        
        query,values = TableSQL.filter_data_sql(self,kwargs)        
        with SQLIteConnection() as conn:
            conn.execute(query,values)
            data = [(dict(zip([column[0] for column in conn.description], row ))) for row in conn.fetchall()]                
            return data
    
    def get(self,**kwargs):  
        """
            This method retrieve a specific data in the database.

            For best use, is preferable to search for data using field with unique values in the database or primary key.
        """       
        query,values = TableSQL.filter_data_sql(self,kwargs)
        with SQLIteConnection() as conn:
            conn.execute(query,values)
            data = [(dict(zip([column[0] for column in conn.description], row ))) for row in conn.fetchall()]
        if len(data) == 1:
            return data[0]
        elif len(data) == 0:
            raise ValueError("No matching record found.")
        else:
            raise ValueError("Multiple matching record found.")

    def all(self):
        query = TableSQL.select_all_sql(self)
        with SQLIteConnection() as conn:
            conn.execute(query)
            data = conn.fetchall()
        return data

    def save(self):
        query,values = TableSQL.insert_data_sql(self)         
        with SQLIteConnection() as conn:
            conn.execute(query,values)
            print("Data recorded successfully.")

    def delete(self,id):
        query,param = TableSQL.delete_data_sql(self,id)
        with SQLIteConnection() as conn:            
            conn.execute(query,param)
            print('Data deleted successfully')