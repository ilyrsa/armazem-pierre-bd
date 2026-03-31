# Armazém do Pierre (Stardew Valley) — Sistema de Vendas

Projeto da disciplina de **Banco de Dados I**.  
Sistema CRUD + módulo de vendas em console para gerenciar o estoque e as compras do armazém do Pierre, inspirado no universo de *Stardew Valley*.

**Tecnologias:** Python 3 · PostgreSQL (via Docker) · psycopg2

---

## Estrutura do projeto

```
banco-de-dados/
├── src/
│   ├── main.py           # Interface de terminal (menus do cliente e funcionário)
│   └── gerenciador.py    # Classe GerenciadorArmazem — toda a lógica SQL
├── db/
│   ├── docker-compose.yml  # Configuração do container PostgreSQL
│   └── setup_banco.py    # DDL + seed: cria tabelas, views, procedures e dados iniciais
├── docs/
│   └── diagrama.pdf      # Diagrama UML do projeto
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Como rodar (do zero)

### 1. Clone o repositório

```bash
git clone https://github.com/ilyrsa/banco-de-dados.git
cd banco-de-dados
```

### 2. Crie e ative o ambiente virtual

O ambiente virtual isola as dependências do projeto e evita conflitos com outros projetos Python na sua máquina.

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

> Quando ativo, o terminal mostrará `(venv)` no início da linha.

### 3. Instale as dependências

Com o venv ativo:
```bash
pip install -r requirements.txt
```

Isso instala o `psycopg2-binary`, que é o driver de conexão Python ↔ PostgreSQL.

### 4. Suba o banco de dados com Docker

É necessário ter o [Docker](https://docs.docker.com/get-docker/) instalado.

**Na primeira vez — baixa a imagem e cria o container:**
```bash
cd db
docker-compose up -d
cd ..
```

Isso cria um container chamado `postgres_fazenda` rodando em segundo plano na porta `5432`.

**Nas próximas vezes — só iniciar o container já existente:**
```bash
docker start postgres_fazenda
```

Para parar:
```bash
docker stop postgres_fazenda
```

Para verificar se está rodando:
```bash
docker ps
```

### 5. Crie as tabelas e popule o banco

Com o container rodando e o venv ativo, execute o script de setup **a partir da pasta raiz do projeto**:

```bash
python db/setup_banco.py
```

Saída esperada:
```
✅ Baú do Pierre resetado! Tabelas, Views e Procedures de Venda criadas com sucesso!
```

> ⚠️ Este script **apaga e recria tudo** do zero. Use sempre que quiser resetar o banco.  
> Na primeira vez é obrigatório rodar. Nas próximas, só se quiser resetar os dados.

### 6. Execute o programa

```bash
python src/main.py
```

---

## Próximas execuções (checklist rápido)

Toda vez que for usar o projeto, confirme:

1. **Docker rodando:** `docker start postgres_fazenda`
2. **Venv ativo:** `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows)
3. **Iniciar:** `python src/main.py`

---

## O que o sistema faz

### Área do Cliente
- Ver catálogo completo ou com filtros (nome, faixa de preço, categoria, fabricado em Mari-PB)
- Realizar compras — informa dados pessoais, escolhe vendedor, monta carrinho e forma de pagamento
- Clientes que torcem pro Flamengo, assistem One Piece e/ou são de Sousa-PB ganham **10% de desconto por critério** (até 30%)
- Compra bloqueada automaticamente se produto não tiver estoque suficiente
- Ver histórico de pedidos pelo ID de cliente

### Área do Funcionário
- **Gerenciar Produtos:** inserir, alterar, remover, pesquisar por nome, listar todos, exibir um, relatório geral do estoque
- **Estoque baixo:** lista produtos com menos de 5 unidades
- **Relatório mensal:** vendas confirmadas por vendedor em qualquer mês/ano

### Formas de pagamento (tema Stardew Valley)
| Opção | Descrição |
|-------|-----------|
| Ouros (G) | Moeda universal de Pelicano |
| Fichas do Cassino Qi | Moeda do salão do Sr. Qi |
| Escambo de Recursos | Troca direta por itens da fazenda |
| Bagas da Floresta | Coleta sazonal vira moeda |
| Cristais de Iridium | Mineral raro — crédito premium |
