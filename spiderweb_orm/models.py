from spiderweb_orm.fields import Field,PasswordField
from spiderweb_orm.sql_utils import TableSQL
from spiderweb_orm.sqlite.sqlite_connection import SQLIteConnection


class ModelMeta(type):
    def __new__(cls,name,bases,attrs):
        fields = {key: value for key, value in attrs.items() if isinstance(value,Field)}
        new_class = super().__new__(cls,name,bases,attrs)
        new_class._fields = fields
        meta = attrs.get('MetaData',None)
        if meta:
            new_class._meta = {}
            for attr_name in dir(meta):
                if not attr_name.startswith('_'):
                    new_class._meta[attr_name] = getattr(meta,attr_name)                
        return new_class
    
class Model(metaclass=ModelMeta):

    class MetaData:   
        rdbms = SQLIteConnection()
    
    def get_meta_attr(self,attr,default=None):
        return self._meta.get(attr, default)
               
    def _rdbms(self):
        return self._meta.get('rdbms')  

    def __init__(self,**kwargs) -> None:
        for key, value in kwargs.items():
            if key in self._fields:
                setattr(self,key,self._fields[key].validate(value))
            else:
                raise AttributeError(f"{key} is not a valid field for {self.__class__.__name__}")
       
    def create_table(self):
        sql,sql_safely_password_store = TableSQL.create_table_sql(self)
        with self._rdbms() as conn:
            conn.execute(sql)
            if sql_safely_password_store:
                conn.execute(sql_safely_password_store)
            print('Table created successfully.')
    
    
    def filter(self,**kwargs):        
        query,values = TableSQL.filter_data_sql(self,kwargs)        
        with self._rdbms() as conn:
            conn.execute(query,values)
            data = [(dict(zip([column[0] for column in conn.description], row ))) for row in conn.fetchall()]                
            return data
    
    def get(self,**kwargs):  
        """
            This method retrieve a specific data in the database.

            For best use, is preferable to search for data using field with unique values in the database or primary key.
        """       
        query,values = TableSQL.filter_data_sql(self,kwargs)
        with self._rdbms() as conn:
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
        with self._rdbms() as conn:
            conn.execute(query)
            data = conn.fetchall()            
        return data

    def save(self):
        normal_insert,has_password = TableSQL.insert_data_sql(self)         
        query, values = normal_insert
        pk = None
        with self._rdbms() as conn:            
            conn.execute(query, values)                    
            conn.execute(f'SELECT * FROM {self.__class__.__name__.lower()};')
            pk = conn.fetchall()[-1][0]           
            if has_password:

                password = None
                conn.execute(f'UPDATE {self.__class__.__name__.lower()} SET passwordID = {pk} WHERE id = {pk};')
                for field_name, field_class in self._fields.items():
                    if isinstance(field_class,PasswordField):
                        password = getattr(self,field_name)
                        salt = field_class.salt 
                        hash_name = field_class.hash  
                        _iter = field_class.iterations 
                
                from hashlib import pbkdf2_hmac

                salt = salt[0]
                _hash = pbkdf2_hmac(
                    hash_name=hash_name,
                    password=password.encode(),
                    salt=salt.to_bytes(),
                    iterations= _iter).hex()       
                query = f"INSERT INTO passwords (id,hash,salt) VALUES ({pk},'{_hash}','{salt}');"            
                conn.execute(query)
            print("Data recorded successfully.")
       
    def delete(self,id):
        query,param = TableSQL.delete_data_sql(self,id)
        with self._rdbms() as conn:            
            conn.execute(query,param)
            print('Data deleted successfully') 

    def update(self,**kwargs):
        query,values = TableSQL().update_data_sql(self,kwargs)        
        with self._rdbms() as conn:
            conn.execute(query,values)  
            print('Data altered successfully.')
