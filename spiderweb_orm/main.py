import os 
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)


from spiderweb_orm import fields, models
from spiderweb_orm.validators.exceptions import ValidationError


# create your models here

class User(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120,null=False)
    email = fields.CharField(max_length=255,null=False)
    password = fields.PasswordField(max_length=128,null=False)
    joined_on = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    is_active = fields.BooleanField(default=True)


class Product(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120)
    price = fields.DecimalField()
    discount = fields.FloatField(default=5.2)
    manufacture_date = fields.DateField(auto_now=True)
    added_on = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    in_stock = fields.BooleanField()

User().create_table()
Product().create_table()

try:
    user_1 = User(
        name = 'Mr. Aguinaldo',
        email = 'mraguinaldo@gmail.com',
        password = 'password413',
        image = 'img1.png',
        )

    user_1.save()    

    product_1 = Product(
        name = 'Laptop425',
        price = 1230.52,
        image = 'laptop2.png',
        in_stock = True
    )

    product_1.save()

except ValidationError as e:
    raise ("Validation error:",e)
