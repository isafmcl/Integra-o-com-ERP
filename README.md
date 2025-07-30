# Painel de Monitoramento de Estoque e Vendas Integrado ao ERP

Sistema de dashboard para monitoramento de estoque e vendas, integrado com banco de dados MySQL, desenvolvido com FastAPI e Streamlit.

## Tecnologias Utilizadas

- Python 3.11+
- FastAPI (API REST)
- Streamlit (Dashboard)
- SQLAlchemy (ORM)
- MySQL (Banco de dados)
- Pandas (Manipulação de dados)
- Plotly (Gráficos interativos)

##  Estrutura do Projeto

```
erp_dashboard/
├── api/
│ ├── main.py         # API FastAPI
│ ├── database.py     # Configuração do banco
│ ├── models.py       # Modelos SQLAlchemy
│ └── crud.py         # Operações no banco
├── dashboard/
│ └── app.py         # Interface Streamlit
├── utils/
│ └── email_alert.py # Sistema de alertas
├── .env             # Configurações
└── requirements.txt # Dependências
```

##  Configuração

1. Clone o repositório
2. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   .\\venv\\Scripts\\activate  
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo `.env` com suas credenciais do MySQL:
   ```
   DB_HOST=localhost
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_NAME=seu_banco
   DB_PORT=3306
   ```

## Executando o Projeto

1. Inicie a API:
   ```bash
   cd api
   uvicorn main:app --reload
   ```

2. Em outro terminal, inicie o dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```

3. Para verificar alertas de estoque:
   ```bash
   cd utils
   python email_alert.py
   ```

## Funcionalidades

### API REST (FastAPI)
- Lista de produtos
- Vendas com filtros (loja, categoria, período)
- Status do estoque
- Alertas de ruptura

### Dashboard (Streamlit)
- Gráficos dinâmicos:
  - Vendas por categoria
  - Curva ABC de produtos
  - Margem de lucro por produto
- Filtros interativos
- Exibição de estoque crítico
- Ranking de produtos mais vendidos

### Sistema de Alertas
- Monitoramento de estoque baixo
- Simulação de envio de alertas por e-mail

## Endpoints da API

- `GET /produtos` - Lista todos os produtos
- `GET /vendas` - Lista vendas com filtros
- `GET /estoque` - Status atual do estoque
- `GET /alertas/ruptura` - Produtos com estoque abaixo do mínimo
- `GET /analytics/vendas-categoria` - Vendas por categoria
- `GET /analytics/curva-abc` - Curva ABC de produtos
- `GET /analytics/margem-lucro` - Margem de lucro por produto
- `GET /analytics/mais-vendidos` - Ranking de produtos mais vendidos

## Documentação da API

Após iniciar a API, acesse:
- Documentação Swagger UI: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc
