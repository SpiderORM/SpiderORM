from MySQLdb import connect, OperationalError

__all__ = ['MysqlConnection']

class MysqlConnection:
    def __init__(self,*args,**kwargs) -> None:
        self.conn = None
        try:
            self.conn = connect(*args,**kwargs,)
        except OperationalError as e:
            database = kwargs.get('database') or kwargs.get('db')            
            _conn = connect(host=kwargs.get('host'),user=kwargs.get('user'),password=kwargs.get('password'))            
            _conn.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {database};')   
            _conn.commit()
            _conn.close()        
        finally:
            self.conn = connect(*args,**kwargs)

    def __enter__(self):        
        return self.conn.cursor()

    def __exit__(self,exc_type,exc_value,exc_to):
        self.conn.commit()
        self.conn.close()

