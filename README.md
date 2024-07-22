
# SpiderWeb ORM

SpiderWeb ORM é um framework ORM (Object-Relational Mapping) leve e flexível para Python. Ele permite que você defina e manipule modelos de dados de maneira intuitiva e com validação robusta.

## Funcionalidades

- Definição de modelos de dados com campos variados (CharField, IntegerField, DecimalField, etc.)
- Suporte a chaves primárias, auto-incremento, valores padrão e unicidade
- Validação robusta de campos, incluindo campos nulos, valores padrão e unicidade
- Suporte a tipos de campos adicionais como ImageField, FileField e URLField
- Criação automática de tabelas no banco de dados
- Inserção de dados com validação
- Suporte a bancos de dados SQLite (pode ser expandido para outros bancos de dados)

## Instalação

Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/seuusuario/spiderweb-orm.git
cd spiderweb-orm
```

Certifique-se de ter o Python 3.6+ instalado no seu sistema. Instale os requisitos (se houver) usando pip:

```bash
pip install -r requirements.txt
```

## Uso

### Definição de Modelos

Defina seus modelos de dados herdando da classe `Model` e especificando os campos desejados:

```python
from models.model import Model
from models.fields import CharField, IntegerField, DecimalField, FloatField, BooleanField, DateField, DateTimeField, ChoiceField, ImageField, FileField, URLField, ForeignKey
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

# Criando a tabela
Product.create_table()
```

### Inserção de Dados

Crie instâncias dos modelos e salve-os no banco de dados:

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

### Validação

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

## Contato

Simão Domingos De Oliveira António
- Email: simaodomingos413@gmail.com
- Telefone: +244 925845239
  
