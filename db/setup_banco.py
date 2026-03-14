import sqlite3
import os

# Arquivo .db vai ser criado dentro da pasta db
# os.path garante que o caminho seja correto independente do sistema operacional
caminho_db = os.path.join(os.path.dirname(__file__), 'banco.db')

# Criando a conexão com o banco de dados (se o arquivo não existir, ele será criado)
conexao = sqlite3.connect(caminho_db)
cursor = conexao.cursor()

# ==========================================
# CRIAÇÃO DAS TABELAS (DDL - Data Definition Language)
# ==========================================

# 1. Tabela de categorias de produtos
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT, -- Chave primária auto-incrementada
    nome TEXT NOT NULL UNIQUE,                      -- UNIQUE para evitar categorias duplicadas
    valor_base REAL NOT NULL                        --  REAL é o tipo do SQLite para valores decimais. NOT NULL manda preencher.
)
''')

# 2. Tabela de qualidades
cursor.execute('''
CREATE TABLE IF NOT EXISTS qualidades (
    id_qualidade INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    multiplicador REAL NOT NULL   
)
''')

# 3. Tabela de produtos
# Não possui a coluna valor_total, pois ela será calculada dinamicamente com base no valor_base da categoria e no multiplicador da qualidade    
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade_estoque INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    id_qualidade INTEGER NOT NULL,

    -- RESTRIÇÕES DE INTEGRIDADE REFERENCIAL
    -- Não é possível inserir um produto com uma categoria ou qualidade que não exista nas tabelas
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_qualidade) REFERENCES qualidades(id_qualidade)
)
''')

# ==========================================
# INSERÇÃO DE DADOS INICIAIS (DML - Data Manipulation Language)
# ==========================================

# Preenchendo a tabela base de dados
# O comando INSERT OR IGNORE é usado para evitar erros caso os dados já existam (por exemplo, se o script for executado mais de uma vez)
cursor.executescript('''
    INSERT OR IGNORE INTO categorias (nome, valor_base) VALUES ('Semente', 20.0);
    INSERT OR IGNORE INTO categorias (nome, valor_base) VALUES ('Fruta', 80.0);
    INSERT OR IGNORE INTO categorias (nome, valor_base) VALUES ('Produto Artesanal', 300.0);
    INSERT OR IGNORE INTO categorias (nome, valor_base) VALUES ('Peixe', 100.0);

    INSERT OR IGNORE INTO qualidades (nome, multiplicador) VALUES ('Normal', 1.0);
    INSERT OR IGNORE INTO qualidades (nome, multiplicador) VALUES ('Prata', 1.25);
    INSERT OR IGNORE INTO qualidades (nome, multiplicador) VALUES ('Ouro', 1.5);
    INSERT OR IGNORE INTO qualidades (nome, multiplicador) VALUES ('Irídio', 2.0);
''')

conexao.commit()
conexao.close()

print("Baú do Stardew Valley construído e preenchido com sucesso na pasta db/")