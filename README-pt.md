# Spider-ORM

Spider-ORM é uma biblioteca ORM (Object-Relational Mapping) em Python projetada para facilitar a interação com bancos de dados relacionais como MySQL e SQLite. Ele permite a definição de modelos de banco de dados como classes Python e fornece uma interface simples para realizar operações de banco de dados, como criação de tabelas, inserção, consulta, filtragem, atualização e exclusão de dados.

## Índice

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
  - [Definição dos Modelos](#definição-dos-modelos)
  - [Operações no Banco de Dados](#operações-no-banco-de-dados)
    - [Criação de Tabelas](#criação-de-tabelas)
    - [Inserção de Dados](#inserção-de-dados)
    - [Consulta de Dados](#consulta-de-dados)
    - [Filtragem de Dados](#filtragem-de-dados)
    - [Atualização de Dados](#atualização-de-dados)
    - [Exclusão de Dados](#exclusão-de-dados)
- [Testes](#testes)
- [Licença](#licença)

## Instalação

Para instalar o Spider-ORM, clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/spider-orm.git
cd spider-orm
pip install -r requirements.txt
```

## Configuração

### Conexão com o Banco de Dados

O Spider-ORM suporta conexão com diferentes SGBDs (Sistemas de Gerenciamento de Banco de Dados). Abaixo está um exemplo de como configurar a conexão com um banco de dados MySQL:

```python
from spiderweb_orm.mysql.connection import MysqlConnection

DB_CONNECTION = MysqlConnection(
    host='localhost',
    user='root',
    password='root',
    database='mysql_db'
)
```

## Uso

### Definição dos Modelos

Defina seus modelos de banco de dados como classes que herdam de `models.Model`. Cada atributo da classe representa um campo na tabela do banco de dados.

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

### Operações no Banco de Dados

#### Criação de Tabelas

Para criar uma tabela no banco de dados baseada em um modelo, utilize o método `create_table()`:

```python
user_table = User()
user_table.create_table()
```

#### Inserção de Dados

Para inserir novos registros na tabela, crie uma instância do modelo e chame o método `save()`:

```python
user = User(
    name='Simon Dev',
    email='simondev@gmail.com',
    password='mypassword',
    image='img.png'
)
user.save()
```

#### Consulta de Dados

Para obter todos os registros de uma tabela, utilize o método `all()`:

```python
users = user_table.all()
```

#### Filtragem de Dados

Filtre registros utilizando o método `filter()`. Exemplo de filtragem por ID e estado ativo:

```python
users_filtered = user_table.filter(id__lt=20, is_active=True)
```

#### Atualização de Dados

Para atualizar registros existentes, use o método `update()`:

```python
user_table.update(email='newemail@gmail.com', id=10)
```

#### Exclusão de Dados

Para excluir registros, utilize o método `delete()`:

```python
user_table.delete(id=1)
```

## Testes

Testes podem ser realizados utilizando `pytest`. Para ignorar falhas e continuar executando os testes, utilize a flag `--continue-on-collection-errors` ou marque os testes que podem falhar com `pytest.mark.xfail`.

```bash
pytest --continue-on-collection-errors
```

Ou, dentro do código de teste:

```python
import pytest

@pytest.mark.xfail
def test_func():
    assert False  # Esta falha será ignorada
```

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

