# Armazém do Pierre — Sistema de Vendas

Projeto da disciplina de **Banco de Dados I**.

Um sistema de CRUD e vendas em console para gerenciar o estoque e as compras do armazém do Pierre, com tema inspirado no jogo Stardew Valley. A interface é dividida entre área do cliente e área do funcionário, com lógica de descontos, histórico de pedidos e relatórios mensais.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

</div>

---

## Estrutura do Projeto

```
armazem-pierre-bd/
├── src/
│   ├── main.py           # Interface de menus (cliente e funcionário)
│   ├── interface.py      # Componentes visuais de terminal (rich)
│   └── gerenciador.py    # Toda a lógica de acesso ao banco de dados
├── db/
│   ├── docker-compose.yml        # Configuração do container PostgreSQL
│   ├── setup_banco.py            # DDL + seed (cria e popula o banco do zero)
│   └── Fazenda Stardew session.sql
├── docs/
│   └── diagrama.pdf      # Diagrama entidade-relacionamento do projeto
├── .env                  # Credenciais do banco (não versionado)
├── requirements.txt      # Dependências Python
└── README.md
```

---

## Primeira Vez: Setup Completo

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/) (com Docker Compose)

### 1. Clonar o repositório

```bash
git clone https://github.com/ilyrsa/armazem-pierre-bd.git
cd armazem-pierre-bd
```

### 2. Criar e ativar o ambiente virtual

O `venv` isola as dependências do projeto e evita conflitos com outros projetos Python.

```bash
python3 -m venv venv
source venv/bin/activate
```

Quando ativo, você verá `(venv)` no início do terminal.

### 3. Instalar as dependências

Com o venv ativado:

```bash
pip install -r requirements.txt
```

Isso instala `psycopg2-binary` (driver Python/PostgreSQL), `python-dotenv` (leitura do `.env`) e `rich` (interface de terminal).

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=stardew
DB_USER=postgres
DB_PASS=1234
```

### 5. Subir o banco de dados (Docker)

Na **primeira vez**, o comando abaixo cria o container PostgreSQL:

```bash
cd db
docker-compose up -d
cd ..
```

Isso sobe um container chamado `postgres_fazenda` na porta `5432`, com volume persistente `stardew_data`.

### 6. Criar e popular o banco

Com o container rodando e o venv ativo, execute a partir da raiz do projeto:

```bash
python db/setup_banco.py
```

Saída esperada:

```
Limpando e recriando o baú...
Baú do Pierre resetado! Tabelas, Views e Procedures de Venda criadas com sucesso!
```

> Este script dropa e recria tudo do zero. Use sempre que quiser reiniciar o estado do banco.

### 7. Rodar a aplicação

```bash
python src/main.py
```

---

## Próximas Sessões

Nas sessões seguintes, basta retomar o container e ativar o ambiente:

```bash
# 1. Iniciar o container do banco
docker start postgres_fazenda

# 2. Ativar o venv
source venv/bin/activate

# 3. Rodar o programa
python src/main.py
```

Para encerrar o container ao final:

```bash
docker stop postgres_fazenda
```

---

## Funcionalidades

### Área do Cliente

| Funcionalidade | Descrição |
|---|---|
| Ver catálogo | Lista todos os produtos com nome, preço calculado, categoria e estoque |
| Filtrar produtos | Por nome, faixa de preço, categoria ou origem (fabricado em Mari-PB) |
| Realizar compra | Cadastro, montagem de carrinho, escolha de vendedor e forma de pagamento |
| Descontos | 10% por critério: torcer pro Flamengo, assistir One Piece ou ser de Sousa-PB (até 30%) |
| Histórico de pedidos | Consulta de compras anteriores pelo ID do cliente |

### Área do Funcionário

| Funcionalidade | Descrição |
|---|---|
| Inserir produto | Cadastra novo item com categoria, qualidade e origem |
| Alterar produto | Atualiza nome e/ou quantidade de estoque |
| Remover produto | Remove um produto pelo ID |
| Pesquisar produto | Busca por trecho do nome |
| Listar produtos | Exibe todos os produtos com categoria e qualidade |
| Detalhes de um produto | Preço final calculado, estoque e atributos |
| Alerta de estoque baixo | Lista produtos com menos de 5 unidades em estoque |
| Relatório mensal | Vendas confirmadas por vendedor em qualquer mês/ano |
| Gerenciar clientes | Lista de clientes cadastrados com seus critérios de desconto |

---

## Banco de Dados

### Tabelas

| Tabela | Descrição |
|---|---|
| `categorias` | Tipos de produto (Semente, Cultivo, Coleta, Peixe…) com valor base |
| `qualidades` | Raridade do produto (Normal, Prata, Ouro, Irídio) com multiplicador de preço |
| `produtos` | Itens do armazém: nome, estoque, categoria, qualidade e origem |
| `clientes` | Cadastro com os três critérios de desconto |
| `vendedores` | Funcionários responsáveis pelas vendas |
| `formas_pagamento` | Métodos de pagamento disponíveis |
| `vendas` | Transações: data, cliente, vendedor, pagamento e valores |
| `itens_venda` | Relação produto ↔ venda (quantidade, preço unitário, subtotal) |

### Views

| View | Descrição |
|---|---|
| `vw_produtos_detalhados` | Produtos com preço final calculado (`valor_base × multiplicador`) |
| `vw_historico_cliente` | Histórico de compras por cliente com forma de pagamento |
| `vw_relatorio_vendas_mensal` | Vendas mensais agrupadas por vendedor com itens vendidos |

### Stored Procedures

| Procedure | Descrição |
|---|---|
| `sp_adicionar_item_venda` | Valida estoque, insere o item na venda e atualiza o valor bruto |
| `sp_finalizar_venda` | Calcula e aplica o desconto, atualiza o valor líquido e confirma a venda |

### Como o preço é calculado

```
preco_venda = categoria.valor_base × qualidade.multiplicador
```

Exemplo: Couve (Cultivo, qualidade Ouro) → `80.0 × 1.50 = 120.0 G`

---

## Configuração do Banco

As credenciais são lidas do arquivo `.env` na raiz do projeto. Os valores padrão são:

| Variável | Valor padrão |
|---|---|
| `DB_HOST` | `127.0.0.1` |
| `DB_PORT` | `5432` |
| `DB_NAME` | `stardew` |
| `DB_USER` | `postgres` |
| `DB_PASS` | `1234` |

Para usar credenciais diferentes, basta editar o `.env`. Os scripts `db/setup_banco.py` e `src/gerenciador.py` já leem tudo a partir dele.

---

## Autoras

Desenvolvido por [@ilyrsa](https://github.com/ilyrsa) e [@bruvaloes](https://github.com/bruvaloes).

---

## Licença

Projeto acadêmico — Banco de Dados I (2026).
