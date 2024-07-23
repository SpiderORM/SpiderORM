import os 
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

from spiderweb_orm import fields,models
from spiderweb_orm.validators.exceptions import ValidationError



class Product(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=100,null=False)
    price = fields.DecimalField()
    discount = fields.FloatField(default=0.2)
    in_stock = fields.BooleanField()
    manufacture_date = fields.DateField(auto_now=True)
    added_on = fields.DateTimeField(auto_now=True)
    category = fields.ChoiceField(choices=['Electronics','Clothing','Food'])
    image = fields.ImageField()
    manual = fields.FileField(allowed_types=['pdf','msword'])
    product_url = fields.URLField()

Product().create_table(Product)


try:
    product = Product(        
        name='Laptop',
        price = 999.9,
        discount=10.5,              
        in_stock = True,       
        category = 'Electronics',
        image = 'laptop3.png',
        manual = 'manual5.pdf',
        product_url = 'https://example.com/product/laptop6'       
    )
    
    product.save()
    print('Product saved successfully.')
except ValidationError as e:
    print(f"Validation error. {e}")