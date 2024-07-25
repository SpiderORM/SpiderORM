""""
    This module is used to test the features created.
    
"""



import os 
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)


from spiderweb_orm import fields, models
from spiderweb_orm.validators.exceptions import ValidationError
from spiderweb_orm.sanitizers import sanitize_string,sanitize_image,sanitize_boolean,sanitize_time,sanitize_decimal


# create your models here

class User(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120,null=False)
    email = fields.EmailField(max_length=255,null=False)
    password = fields.PasswordField(max_length=128,null=False)
    joined_on = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    is_active = fields.BooleanField(default=True)


class Product(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120)
    price = fields.DecimalField(max_digits=12,decimal_places=3)
    discount = fields.FloatField(default=5.2)
    manufacture_date = fields.DateField(auto_now=True)
    added_on = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    in_stock = fields.BooleanField()

class Runner(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120,null=False)
    email = fields.EmailField(max_length=255,null=False)
    arrive_time = fields.TimeField()
    

# Runner().create_table()

# User().create_table()
# Product().create_table()

try:
    # user_1 = User(
    #     name = 'Mr. Aguinaldo',
    #     email = 'mraguinaldo@gmail.com',
    #     password = 'password413',
    #     image = 'img12.png',
    #     )

    # user_1.save()    

    # product_1 = Product(
    #     name = 'Laptop425',
    #     price = 1230.52,
    #     image = 'laptop2.png',
    #     in_stock = True
    # )
    
    product_2 = Product(
        name = sanitize_string('Laptop5'),
        price = sanitize_decimal(1500.522500),
        image = sanitize_image('laptop635.png'),
        in_stock = sanitize_boolean('true')
    )

    # product_3 = Product(
    #     name = 'DesktopLenovo',
    #     price = 5220.52,
    #     image = 'laptop35.png',
    #     in_stock = True
    # )

    # import datetime
    # product_4 = Product(
    #     name = 'DesktopLenovo',
    #     price = 5220.52,
    #     manufacture_date=datetime.date(2024,5,3),
    #     image = 'laptop55r.png',
    #     in_stock = True
    # )

    # product_1.save()
    product_2.save()
    # product_3.save()
    # product_4.save()
    
    runner_1 = Runner(
        name=sanitize_string('John Speed'),
        email=sanitize_string('john@gmail.com'),        
        arrive_time= sanitize_time('00:03:52'))

    # runner_1.save()

except ValidationError as e:
    raise e


products = Product().filter(price__gt=100,discount__lt=10)

# products = Product().filter(price__gte=5000)

# products = Product().filter(price__bt=(1000,6000),manufacture_date__lte='2024-05-03')
print(products)

# runners = Runner().filter(name='John Speed')
# print(runners)