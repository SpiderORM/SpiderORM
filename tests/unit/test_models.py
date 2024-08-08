import pytest
import os 
import sys

path = os.path.dirname(os.path.abspath('.'))
for root, dirs, files in os.walk(path):
    for _dir in dirs:
        sys.path.append(_dir)

from spiderweb_orm.models import Model
from spiderweb_orm import fields
from spiderweb_orm.sqlite.sqlite_connection import SQLIteConnection

class Product(Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)

    class MetaData:
        rdbms = SQLIteConnection()
@pytest.mark.xfail
def test_get(id=1):
    product = Product().get(id=id)

    with SQLIteConnection() as conn:
        conn.execute(f'SELECT * FROM product where id = {id}')
        expected = [(dict(zip([column[0] for column in conn.description], row ))) for row in conn.fetchall()]
    assert product == expected[0]

def test_get_not_found(id=10e100):
    with pytest.raises(ValueError):
        product = Product().get(id=id)
   
