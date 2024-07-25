
# SpiderWeb ORM

SpiderWeb ORM é uma biblioteca de mapeamento objeto-relacional (ORM) escrita em Python, desenvolvida para facilitar a interação entre Objetos Pyhon e um banco de dados relacional. Ele permite que você defina e manipule modelos de dados de maneira intuitiva e com validação robusta através de Objectos Python.

## Rescursos

- Definição de modelos de dados com campos variados:
    - **CharField**
    - **IntegerField**
    - **DecimalField**
    - **FloatField** 
    - **DateField**
    - **DateTimeField**
    - **BooleanField**
 
- Suporte a chaves primárias, auto-incremento, valores padrão e unicidade
- Suporte a chaves estrangeiras
- Validação robusta de campos, incluindo campos nulos, valores padrão e unicidade
- Suporte a tipos de campos adicionais como **ImageField**, **FileField**, **URLField**, **EmailField** e **PasswordField**
- Criação automática de tabelas no banco de dados
- Inserção de dados com validação
- Filtragem de dados avançadas
- Suporte a bancos de dados SQLite (posteriormente será expandido para outros bancos de dados)

## Instalação

Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/yourusername/spiderweb-orm.git
cd spiderweb-orm
```

Certifique se de ter o Python 3.6 instalado na sua máquina. Instala as dependencias (se houver) usando o seguinte comando:

```bash
pip install -r requirements.txt
```


## Exemplo de uso

### Definição de Modelos

Defina seus modelos de dados herdando da classe `Model` e especificando os campos desejados:

```python
from spiderweb_orm import fields, models
from spiderweb_orm.validators.exceptions import ValidationError


# create your models here

class User(models.Model):
    id = fields.IntegerField(primary_key=True,auto_increment=True)
    name = fields.CharField(max_length=120,null=False)
    email = fields.EmailField(max_length=255,null=False)
    password = fields.PasswordField(max_length=32,null=False)
    age = fields.IntegerField(null=False)
    joined_at = fields.DateTimeField(auto_now=True)
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

# Criando as tabelas 
User().create_table()
Product().create_table()
```

### Inserção de Dados

Crie instâncias dos modelos e salve-os no banco de dados:

```python
try:
    # Criando instâncias do tipo User
    user_1 = User(
        name = 'Simon Dev',
        email = 'simondev413@gmail.com',
        password = 'password413',
        age = 23,
        image = 'img-simon-dev.png',
        ) 

    #Salvando os dados na base de dados
    user_1.save()    
   

    # Criando instâncias do tipo Product
    product_1 = Product(
        name = 'Lenovo Ideapad 145s',
        price = 1200.52,
        image = 'laptop-ln.png',
        in_stock = True
    )

    #Salvando os dados na base de dados
    product_1.save()

except ValidationError as e:
    print(f"Validation error: {e}")
```

### Buscando dados

Filtragem simples para buscar dados usando o metódo **get**:

```python
user = User.get(name='Simon Dev')
print(user)
```
#### Filtragem avançada

Para usar filtros avançados com **lt** (menor que), **gt** (maior que), **lte** (menor ou igual a), **gte** (maior ou igual a), **bt** (entre):

Usando o **lt** (menor que):
```python
users = User().filter(age__lt=30)
print(users) # Retorna todos os usuários com idade inferior a 30

```
Usando o **gt** (maior que):
```python
users = User().filter(age__gt=20)
print(users) # Retorna todos os usuários com idade superior a 20

```
Usando o **lte** (menor ou igual a):
```python
users = User().filter(age__lte=23)
print(users) # Retorna todos os usuários com idade inferior ou igual a 23
```
Usando o **gte** (maior ou igual a):
```python
users = User().filter(age__gte=23)
print(users) # Retorna todos os usuários com idade superior ou igual a 23
```
Usando o **bt** (entre):
```python
products = Product().filter(price__bt=(1000,6000))
print(products) # Retorna todos os produtos com o preço entre 1000 à 6000
```

### Validação de campos

Os campos são validados automaticamente antes de serem salvos no banco de dados. As validações incluem:

- Verificação de campos nulos
- Aplicação de valores padrão
- Verificação de unicidade
- Validação específica por tipo de campo (e.g., tamanho máximo de strings)

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

1. Faça um fork do projeto
2. Crie um branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Faça um push para o branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.