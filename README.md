# SpiderWeb ORM

SpiderWeb ORM é uma biblioteca de mapeamento objeto-relacional (ORM) em Python, desenvolvida para facilitar a interação entre objetos Python e um banco de dados relacional. Este ORM fornece classes e métodos para definir, validar e manipular modelos de dados, além de executar operações CRUD (Create, Read, Update, Delete).

## Recursos

- Suporte a diversos tipos de campos (CharField, IntegerField, DecimalField, FloatField, BooleanField, DateField, DateTimeField, ChoiceField, ImageField, FileField, URLField, EmailField, PasswordField).
- Validação de campos e tratamento de erros.
- Suporte a chaves estrangeiras.
- Métodos para criação de tabelas e inserção, busca e filtragem de dados.
- Tratamento de saneamento de entrada para proteção contra ataques de injeção SQL.
- Conexão com banco de dados SQLite.

## Instalação

Para instalar o SpiderWeb ORM, você pode clonar o repositório do GitHub:

```bash
git clone https://github.com/seuusuario/spiderweb_orm.git
cd spiderweb_orm
```

## Uso

### Definindo um Modelo

Para definir um modelo, crie uma classe que herde de `Model` e adicione atributos de campo:

```python
from spiderweb_orm.fields import CharField, IntegerField, EmailField, PasswordField
from spiderweb_orm.models import Model

class User(Model):
    id = IntegerField(primary_key=True, auto_increment=True)
    username = CharField(max_length=100, unique=True, null=False)
    email = EmailField(max_length=255, unique=True, null=False)
    password = PasswordField(max_length=255, null=False)
    age = IntegerField(null=False)

# Criação da tabela
User().create_table()
```

### Inserindo Dados

Para inserir dados, crie uma instância do modelo e chame o método `save`:

```python
user = User(username="john_doe", email="john@example.com", password="mypassword", age=30)
user.save()
```

### Buscando Dados

#### Filtragem Simples

Para buscar dados com filtros simples:

```python
user = User().get(username="john_doe")
print(user)
```

#### Filtragem Avançada

Para usar filtros avançados como lt (menor que), gt (maior que), lte (menor ou igual a), gte (maior ou igual a), e bt (entre):

```python
users = User().filter(age__gt=20, age__lt=40)
print(users)
```

### Todos os Dados

Para obter todos os dados de uma tabela:

```python
all_users = User().all()
print(all_users)
```

### Excluindo Dados

Para excluir um registro:

```python
user = User().get(id=1)
user.delete(user.id)
```

## Validações

O módulo `validators.fields.py` contém funções de validação para diferentes tipos de campos, garantindo a integridade dos dados antes de serem salvos no banco de dados.

### Validações Implementadas

- `validate_required`
- `validate_null`
- `validate_string`
- `validate_integer`
- `validate_float`
- `validate_decimal`
- `validate_boolean`
- `validate_date`
- `validate_datetime`
- `validate_choices`
- `validate_url`
- `validate_file_type`
- `validate_default`
- `validate_email`

## Exemplos de Uso

Aqui estão alguns exemplos de como usar o ORM em um projeto Python.

```python
from spiderweb_orm.fields import CharField, IntegerField
from spiderweb_orm.models import Model

class Product(Model):
    id = IntegerField(primary_key=True, auto_increment=True)
    name = CharField(max_length=100, unique=True, null=False)
    price = IntegerField(null=False)

# Criação da tabela
Product().create_table()

# Inserindo um produto
product = Product(name="Laptop", price=1000)
product.save()

# Buscando um produto
product = Product().get(name="Laptop")
print(product)

# Excluindo um produto
product.delete(product.id)
```

---

## Contribuição

Para contribuir com o SpiderWeb ORM, siga estas etapas:

1. Faça um fork do repositório.
2. Crie um branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça um push para o branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
