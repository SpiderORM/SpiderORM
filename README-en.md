# SpiderWeb ORM

SpiderWeb ORM is an object-relational mapping (ORM) library written in Python, designed to facilitate interaction between Python objects and a relational database. It allows you to define and manipulate data models intuitively and with robust validation through Python objects.

## Features

- Definition of data models with various fields:
    - **CharField**
    - **IntegerField**
    - **DecimalField**
    - **FloatField**
    - **DateField**
    - **DateTimeField**
    - **BooleanField**
 
- Support for primary keys, auto-increment, default values, and uniqueness
- Support for foreign keys
- Robust field validation, including null fields, default values, and uniqueness
- Support for additional field types such as **ImageField**, **FileField**, **URLField**, **EmailField**, and **PasswordField**
- Automatic creation of tables in the database
- Data insertion with validation
- Advanced data filtering
- Support for SQLite databases (to be expanded to other databases later)

## Installation

To install SpiderWeb ORM, you can clone the GitHub repository:

```bash
git clone https://github.com/yourusername/spiderweb-orm.git
cd spiderweb-orm
```

Ensure you have Python 3.6 installed on your machine. Install the dependencies (if any) using the following command:

```bash
pip install -r requirements.txt
```

## Usage Example

### Defining a Model

To define a model, create a class that inherits from `Model` and add field attributes:

```python
from spiderweb_orm import fields, models
from spiderweb_orm.validators.exceptions import ValidationError

# create your models here

class User(models.Model):
    id = fields.IntegerField(primary_key=True, auto_increment=True)
    name = fields.CharField(max_length=120, null=False)
    email = fields.EmailField(max_length=255, null=False)
    password = fields.PasswordField(max_length=32, null=False)
    age = fields.IntegerField(null=False)
    joined_at = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    is_active = fields.BooleanField(default=True)

class Product(models.Model):
    id = fields.IntegerField(primary_key=True, auto_increment=True)
    name = fields.CharField(max_length=120)
    price = fields.DecimalField()
    discount = fields.FloatField(default=5.2)
    manufacture_date = fields.DateField(auto_now=True)
    added_on = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    in_stock = fields.BooleanField()

# Creating the tables 
User().create_table()
Product().create_table()
```

### Inserting Data

Create instances of the models and save them to the database:

```python
try:
    # Creating instances of type User
    user_1 = User(
        name='Simon Dev',
        email='simondev413@gmail.com',
        password='password413',
        age=23,
        image='img-simon-dev.png',
    ) 

    # Saving the data to the database
    user_1.save()    
   
    # Creating instances of type Product
    product_1 = Product(
        name='Lenovo Ideapad 145s',
        price=1200.52,
        image='laptop-ln.png',
        in_stock=True
    )

    # Saving the data to the database
    product_1.save()

except ValidationError as e:
    print(f"Validation error: {e}")
```

### Querying Data

Simple filtering to query data using the **get** method:

```python
user = User.get(name='Simon Dev')
print(user)
```

#### Advanced Filtering

To use advanced filters with **lt** (less than), **gt** (greater than), **lte** (less than or equal to), **gte** (greater than or equal to), **bt** (between):

Using **lt** (less than):
```python
users = User().filter(age__lt=30)
print(users) # Returns all users with age less than 30
```

Using **gt** (greater than):
```python
users = User().filter(age__gt=20)
print(users) # Returns all users with age greater than 20
```

Using **lte** (less than or equal to):
```python
users = User().filter(age__lte=23)
print(users) # Returns all users with age less than or equal to 23
```

Using **gte** (greater than or equal to):
```python
users = User().filter(age__gte=23)
print(users) # Returns all users with age greater than or equal to 23
```

Using **bt** (between):
```python
products = Product().filter(price__bt=(1000,6000))
print(products) # Returns all products with price between 1000 and 6000
```

### Field Validation

Fields are automatically validated before being saved to the database. Validations include:

- Null field checks
- Application of default values
- Uniqueness checks
- Type-specific validation (e.g., maximum string length)

## Contribution

To contribute to SpiderWeb ORM, follow these steps:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
