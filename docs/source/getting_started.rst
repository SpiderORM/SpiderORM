Getting Started
===============

Spider-ORM simplifies working with relational databases by using Python objects. Follow these steps to get started with Spider-ORM:

1. **Setup a Database Connection**

   Begin by creating a database connection. For instance, to connect to a MySQL database, use:

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

2. **Create Models**

   Define your data models by creating classes that inherit from `models.Model`. Use Spider-ORM's field types to specify the attributes:

   .. code-block:: python

       class User(models.Model):
           id = fields.IntegerField(primary_key=True, auto_increment=True)
           name = fields.CharField(max_length=120, null=False)
           email = fields.EmailField(max_length=255, null=False)
           password = fields.PasswordField(max_length=128, null=False)
           joined_on = fields.DateTimeField(auto_now=True)
           image = fields.ImageField()
           is_active = fields.BooleanField(default=True)
           
           class MetaData:
               rdbms = DB_CONNECTION

        
        # You can create a model without specifying the RDBMS
        # By default Spider-ORM uses SQLite3
       class Product(models.Model):
           id = fields.IntegerField(primary_key=True, auto_increment=True)
           name = fields.CharField(max_length=120)
           price = fields.DecimalField(max_digits=12, decimal_places=3)
           discount = fields.FloatField(default=5.2)
           manufacture_date = fields.DateField(auto_now=True)
           added_on = fields.DateTimeField(auto_now=True)
           image = fields.ImageField()
           in_stock = fields.BooleanField()

3. **Create Tables**

   To create tables in the database, instantiate your models and call the `create_table` method:

   .. code-block:: python

       user_table = User()
       user_table.create_table()

       product_table = Product()
       product_table.create_table()

4. **Insert Data**

   Create instances of your models and save them to the database:

   .. code-block:: python

       user = User(
           name='Simon Dev',
           email='simondev@gmail.com',
           password='mypassword',
           image='img.png'
       )
       product = Product(
           name='Laptop',
           price=1200.32,
           image='img.jpg',
           in_stock=True
       )

       # Save data in the database
       user.save()
       product.save()

5. **Retrieve Data**

   Retrieve data from the database using methods provided by Spider-ORM:

   .. code-block:: python

       # Get all users and products
       users = user_table.all()
       products = product_table.all()

       # Retrieve specific records by ID
       user_1 = user_table.get(id=1)
       product_1 = product_table.get(id=1)

6. **Filter Data**

   Use filter methods to find records that match specific conditions:

   .. code-block:: python

       # Filter users with id less than 20 and active
       users_filtered = user_table.filter(id__lt=20, is_active=True)

       # Filter products with price between 1000 and 3000 and discount greater than 5
       products_filtered = product_table.filter(price__bt=(1000, 3000), discount__gt=5)

7. **Delete Data**

   Delete records from the database:

   .. code-block:: python

       # Delete user with id = 1
       user_table.delete(id=1)

       # Delete product with id = 2
       product_table.delete(id=2)

8. **Update Data**

   Update existing records:

   .. code-block:: python

       # Update user email
       user_table.update(email='newemail@gmail.com', id=10)

       # Update product name and price
       product_table.update(name='New Name', price=12)

For more detailed usage and advanced features of Spider-ORM, refer to the full documentation.
