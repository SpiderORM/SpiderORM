import sqlite3
import os 
import sys

path = os.path.dirname(os.path.abspath('.'))
for root, dirs, files in os.walk(path):
    for _dir in dirs:
        sys.path.append(_dir)

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

from spiderweb_orm.models import Model
from spiderweb_orm import fields

class Product(Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)

def test_get(id=2):
    product = Product().get(id=id)
    cursor.execute(f'SELECT * FROM product where id = {id}')
    expected = [(dict(zip([column[0] for column in cursor.description], row ))) for row in cursor.fetchall()]
    assert product == expected[0]