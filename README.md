# Budgetsize

Sistema de controle financeiro pessoal e empresarial desenvolvido com Django e TailwindCSS.

## Requisitos

- Python 3.8+
- PostgreSQL
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados PostgreSQL e atualize as configurações em `.env`

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## Funcionalidades

- Autenticação de usuários
- Dashboard com indicadores financeiros
- Gestão de receitas e despesas
- Categorização de transações
- Cadastro de carteiras de investimento (ações e FIIs)
- Relatórios e gráficos
- Interface responsiva 