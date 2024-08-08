# Spider-ORM

Spider-ORM is a Python ORM (Object-Relational Mapping) library designed to simplify interactions with relational databases like MySQL and SQLite. It allows you to define database models as Python classes and provides a simple interface for performing database operations such as table creation, data insertion, querying, filtering, updating, and deletion.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Defining Models](#defining-models)
  - [Database Operations](#database-operations)
    - [Creating Tables](#creating-tables)
    - [Inserting Data](#inserting-data)
    - [Querying Data](#querying-data)
    - [Filtering Data](#filtering-data)
    - [Updating Data](#updating-data)
    - [Deleting Data](#deleting-data)
- [Testing](#testing)
- [License](#license)

## Installation

To install Spider-ORM, clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/spider-orm.git
cd spider-orm
pip install -r requirements.txt
```

## Configuration

### Database Connection

Spider-ORM supports connecting to different DBMSs (Database Management Systems). Below is an example of how to configure a MySQL database connection:

```python
from spiderweb_orm.mysql.connection import MysqlConnection

DB_CONNECTION = MysqlConnection(
    host='localhost',
    user='root',
    password='root',
    database='mysql_db'
)
```

## Usage

### Defining Models

Define your database models as classes that inherit from `models.Model`. Each class attribute represents a field in the database table.

```python
from spiderweb_orm import fields, models

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
```

### Database Operations

#### Creating Tables

To create a table in the database based on a model, use the `create_table()` method:

```python
user_table = User()
user_table.create_table()
```

#### Inserting Data

To insert new records into the table, create an instance of the model and call the `save()` method:

```python
user = User(
    name='Simon Dev',
    email='simondev@gmail.com',
    password='mypassword',
    image='img.png'
)
user.save()
```

#### Querying Data

To retrieve all records from a table, use the `all()` method:

```python
users = user_table.all()
```

#### Filtering Data

Filter records using the `filter()` method. Example of filtering by ID and active status:

```python
users_filtered = user_table.filter(id__lt=20, is_active=True)
```

#### Updating Data

To update existing records, use the `update()` method:

```python
user_table.update(email='newemail@gmail.com', id=10)
```

#### Deleting Data

To delete records, use the `delete()` method:

```python
user_table.delete(id=1)
```

## Testing

Tests can be run using `pytest`. To ignore failures and continue running tests, use the `--continue-on-collection-errors` flag or mark tests that may fail with `pytest.mark.xfail`.

```bash
pytest --continue-on-collection-errors
```

Or, within the test code:

```python
import pytest

@pytest.mark.xfail
def test_func():
    assert False  # This failure will be ignored
```

## License

This project is licensed under the [MIT License](LICENSE).
