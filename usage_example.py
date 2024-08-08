""""
    This module is used to test the features created.
    
"""



import os 
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)


from spiderweb_orm import fields, models
from spiderweb_orm.mysql.connection import MysqlConnection

# Create a DB Connection
DB_CONNECTION = MysqlConnection(
    host='localhost',
    user='root',
    password='root',
    database='mysql_db')

# Create your models here
class User(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120,null=False)
    email = fields.EmailField(max_length=255,null=False)
    password = fields.PasswordField(max_length=128,null=False)
    joined_on = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    is_active = fields.BooleanField(default=True)
    
    class MetaData:
        rdbms = DB_CONNECTION

# You can create a model without specifying the RDBMS
# By default Spider-ORM uses SQLite3
class Product(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120)
    price = fields.DecimalField(max_digits=12,decimal_places=3)
    discount = fields.FloatField(default=5.2)
    manufacture_date = fields.DateField(auto_now=True)
    added_on = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    in_stock = fields.BooleanField()



# Creating Table
user_table =  User()
user_table.create_table()

product_table = Product()
product_table.create_table()


# Inserting Data
user = User(
    name = 'Simon Dev',
    email = 'simondev@gmail.com',
    password = 'mypassword',
    image ='img.png'
)
product = Product(
    name = 'Laptop',
    price = 1200.32,
    image = 'img.jpg',
    in_stock = True
)

# Saving data in database
user.save()
product.save()

# Get data
users =  user_table.all()
products = product_table.all()


# Filter data with get method
user_1 = user_table.get(id=1)   # retrieve user with id = 1 
product_1 = product_table.get(id=1)     # retrieve product with id = 1

# Filter data with method filter
# retrieve all active users with id less than 20
users_filtered = user_table.filter(id__lt=20,is_active=True)    

# retrieve all products with price between 1000 and 3000 
# and discount great than 5
products_filtered = product_table.filter(price__bt=(1000,3000),discount__gt=5)  


# Deleting Data
# Delete user with id = 1
user_table.delete(id=1)
# Delete product with id = 1
product_table.delete(id=2)


# Update Data

user_table.update(email='newemail@gmail.com',id=10)
product_table.update(name='New Name',price=12)