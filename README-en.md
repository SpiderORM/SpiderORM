# SpiderWeb ORM

SpiderWeb ORM is a lightweight and flexible ORM (Object-Relational Mapping) framework for Python. It allows you to define and manipulate data models intuitively and with robust validation.

## Features

- Definition of data models with various fields (CharField, IntegerField, DecimalField, etc.)
- Support for primary keys, auto-increment, default values, and uniqueness
- Robust field validation, including null fields, default values, and uniqueness
- Support for additional field types like ImageField, FileField, and URLField
- Automatic table creation in the database
- Data insertion with validation
- Support for SQLite databases (can be expanded to other databases)

## Installation

Clone the repository to your local environment:

```bash
git clone https://github.com/yourusername/spiderweb-orm.git
cd spiderweb-orm
```

Make sure you have Python 3.6+ installed on your system. Install the requirements (if any) using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Model Definition

Define your data models by inheriting from the `Model` class and specifying the desired fields:

```python
from spiderweb_orm.models import Model
from spiderweb_orm.fields import CharField, IntegerField, DecimalField, FloatField, BooleanField, DateField, DateTimeField, ChoiceField, ImageField, FileField, URLField, ForeignKey
from datetime import date, datetime
from decimal import Decimal

class Product(Model):
    id = IntegerField(primary_key=True, auto_increment=True)
    name = CharField(max_length=100, primary_key=False, null=False, unique=True)
    price = DecimalField(primary_key=False, null=False)
    discount = FloatField(primary_key=False, null=True, default=0.0)
    in_stock = BooleanField(primary_key=False, null=False, default=True)
    manufacture_date = DateField(primary_key=False, null=True)
    added_on = DateTimeField(primary_key=False, null=True, default=datetime.now)
    category = ChoiceField(choices=['Electronics', 'Clothing', 'Food'], primary_key=False, null=False)
    image = ImageField(primary_key=False, null=True)
    manual = FileField(allowed_types=['application/pdf', 'application/msword'], primary_key=False, null=True)
    product_url = URLField(primary_key=False, null=True)

# Creating the table
Product.create_table()
```

### Data Insertion

Create instances of the models and save them to the database:

```python
try:
    product = Product(
        name="Laptop",
        price=Decimal('999.99'),
        discount=10.5,
        in_stock=True,
        manufacture_date=date(2023, 6, 1),
        category="Electronics",
        image="laptop.png",
        manual="manual.pdf",
        product_url="https://example.com/product/laptop"
    )
    product.save()
    print("Product saved successfully")
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Validation

Fields are automatically validated before being saved to the database. Validations include:

- Null field checks
- Default value application
- Uniqueness checks
- Type-specific validation (e.g., maximum string length)

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Simão Domingos De Oliveira António
- Email: simaodomingos413@gmail.com
- Phone: +244 925845239
