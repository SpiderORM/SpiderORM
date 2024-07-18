import os 
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

from spiderweb_orm import fields,models
from spiderweb_orm.validators.exceptions import ValidationError
from datetime import date, datetime


class Product(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=100,null=False)
    price = fields.DecimalField()
    discount = fields.FloatField(default=0.0)
    in_stock = fields.BooleanField()
    manufacture_date = fields.DateField()
    added_on = fields.DateTimeField(default=datetime.now().__str__())
    category = fields.ChoiceField(choices=['Electronics','Clothing','Food'])
    image = fields.ImageField()
    manual = fields.FileField(allowed_types=['pdf','msword'])
    product_url = fields.URLField()

Product().create_table(Product)


try:
    product = Product(
        name='Laptop',
        price = 999.9,
        discount = 10.5,
        in_stock = True,
        manufacture_date = date(2023,6,3),
        category = 'Electronics',
        image = 'laptop.png',
        manual = 'manual.pdf',
        product_url = 'https://example.com/product/laptop'
    )
    
    product.save()
    print('Product saved successfully.')
except ValidationError as e:
    print(f"Validation error. {e}")