# 🌻 Armazém do Pierre — Sistema de Vendas Stardew Valley

**Projeto da disciplina de Banco de Dados I**  
O presente projeto é um sistema completo de CRUD e vendas em console Python para gerenciar estoque e compras do armazém do Pierre, inspirado no jogo Stardew Valley.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-green?style=flat-square)  
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat-square)

</div>

---

## Estrutura do Projeto

```
banco-de-dados/
├── src/
│   ├── main.py                      # Interface terminal (menus cliente e funcionário)
│   └── gerenciador.py               # Lógica SQL aqui
├── db/
│   ├── docker-compose.yml           # Configuração PostgreSQL (container)
│   ├── setup_banco.py               # DDL + seed (tabelas, views, dados iniciais)
│   └── Fazenda Stardew session.sql  # SQL extra
├── docs/
├── requirements.txt                 # Dependências Python
├── .gitignore
└── README.md
```

---

## 🚀 Setup Completo

### Pré-requisitos
- **Python 3.7+**
- **Docker** ([instale aqui](https://docs.docker.com/get-docker/))
- **pip** (gerenciador de pacotes Python)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/ilyrsa/banco-de-dados.git
cd banco-de-dados
```

### Passo 2: Criar e Ativar o Ambiente Virtual

O venv isola as dependências do projeto (evita conflitos com outros projetos).

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

> Quando ativo, você verá `(venv)` no início do terminal

### Passo 3: Instalar Dependências

Com o venv **ativado**:
```bash
pip install -r requirements.txt
```

Isso instala `psycopg2-binary` (driver Python ↔ PostgreSQL).

### Passo 4: Iniciar o Banco de Dados (Docker)

**Na primeira vez — cria o container:**
```bash
cd db
docker-compose up -d
cd ..
```

Isso cria um container chamado `postgres_fazenda` na porta `5432`.

**Das próximas vezes — só inicie o container:**
```bash
docker start postgres_fazenda
```

**Para parar:**
```bash
docker stop postgres_fazenda
```

**Verificar status:**
```bash
docker ps
```

### Passo 5: Popular o Banco de Dados

Com Docker rodando e venv ativo, execute na pasta raiz:

```bash
python db/setup_banco.py
```

Saída esperada:
```
Baú do Pierre resetado! Tabelas, Views e Procedures de Venda criadas com sucesso!
```

🔄 **Este script reseta tudo!** Use-o sempre que quiser começar do zero.

### Passo 6: Executar a Aplicação

```bash
python src/main.py
```

Você verá:
```
=== 🌻 BEM-VINDO(A) AO ARMAZÉM DO PIERRE (Stardew Valley) 🌻 ===

=== MENU PRINCIPAL ===
1. Área do Cliente (Navegar / Comprar / Histórico)
2. Área do Funcionário (Armazém / Relatórios / Clientes)
0. Sair
```

---

## Checklist para Próximas Sessões

Toda vez que quiser usar o sistema, execute na pasta raiz:

```bash
# 1. Inicie o Docker
docker start postgres_fazenda

# 2. Ative o venv
source venv/bin/activate          # Linux/macOS
# ou
venv\Scripts\activate             # Windows

# 3. Rode o programa
python src/main.py
```

---

## Funcionalidades

### Área do Cliente

| Funcionalidade | Descrição |
|---|---|
| **Ver Catálogo** | Listar todos os produtos com nome, preço, categoria e estoque |
| **Filtrar** | Por nome, faixa de preço, categoria ou origem (Mari-PB) |
| **Realizar Compra** | Fazer cadastro, montar carrinho, escolher vendedor e forma de pagamento |
| **Descontos** | 10% por cada critério (Flamengo + One Piece + Sousa-PB = até 30%) |
| **Histórico** | Consultar pedidos anteriores pelo ID de cliente |

### Área do Funcionário

| Funcionalidade | Descrição |
|---|---|
| **Gerenciar Produtos** | Inserir, alterar, remover, pesquisar, listar e exibir detalhes |
| **Alerta Estoque Baixo** | Ver produtos com < 5 unidades em estoque |
| **Relatório Mensal** | Vendas confirmadas por vendedor em qualquer mês/ano |
| **Gerenciar Clientes** | Ver lista de clientes cadastrados e seus critérios de desconto |

---

## Formas de Pagamento (Inspiradas em Stardew Valley)

| Forma | Descrição |
|-------|-----------|
| 💛 **Ouros (G)** | Moeda universal de Pelicano |
| 🎰 **Fichas do Cassino Qi** | Moeda do salão do Sr. Qi |
| 🌾 **Escambo de Recursos** | Troca direta por itens da fazenda |
| 🫐 **Bagas da Floresta** | Coleta sazonal vira moeda |
| 💎 **Cristais de Iridium** | Mineral raro — crédito premium |

---

## Estrutura do Banco de Dados

**Tabelas principais:**
- `produtos` — Item do armazém (nome, estoque, categoria, qualidade, origem)
- `categorias` — Tipo de produto (Semente, Cultivo, Coleta, Peixe)
- `qualidades` — Raridade (Normal, Prata, Ouro, Iridium)
- `clientes` — Cadastro de clientes com os critérios de desconto
- `vendedores` — Funcionários da loja
- `vendas` — Transações (data, vendedor, cliente, forma de pagamento, valores)
- `itens_venda` — Produtos em cada venda (relação muitos-para-muitos)
- `formas_pagamento` — Métodos de pagamento disponíveis

**Views:**
- `vw_produtos_detalhados` — Produtos com preço final calculado
- `vw_historico_cliente` — Histórico de compras por cliente
- `vw_relatorio_vendas_mensal` — Vendas mensais por vendedor

---

## Configuração do Banco

**Credenciais padrão** (`setup_banco.py`):
- **Host:** localhost
- **Database:** stardew
- **User:** lari
- **Password:** 1234
- **Port:** 5432

> ⚠️ Para usar credenciais diferentes, edite `db/setup_banco.py` e `src/gerenciador.py`

---

## 👨‍💻 Desenvolvido por
**Lari e Bruna**

---

## 📝 Licença
Projeto acadêmico (2026)
