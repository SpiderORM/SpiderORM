Database Connections
====================

Supported Database Types
------------------------
- **SQLite**: Default connection, no additional configuration required.
- **MySQL**: Requires explicit configuration.

Creating a Connection
----------------------
By default, the framework uses the SQLite connection. To use MySQL, you must specify the desired connection in the `MetaData` class of your model. See the example below:

   .. code-block:: python

       from spider import fields, models
       from spider.mysql.connection import MysqlConnection

       # Create a DB Connection
       DB_CONNECTION = MysqlConnection(
           host='localhost',
           user='root',
           password='root',
           database='mysql_db'
       )
    
       # Define your model
       class User(models.Model):
           ...
           class MetaData:
               rdbms = DB_CONNECTION
       
       # You can create a model without specifying the RDBMS
       # By default Spider-ORM uses SQLite3    
