import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def resetar_banco():
    config = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASS", "1234"),
        "port": os.getenv("DB_PORT", "5432")
    }

    try:
        conn_temp = psycopg2.connect(database="postgres", **config)
        conn_temp.autocommit = True
        with conn_temp.cursor() as cursor_temp:
            cursor_temp.execute("SELECT 1 FROM pg_database WHERE datname = 'stardew'")
            if not cursor_temp.fetchone():
                cursor_temp.execute("CREATE DATABASE stardew")
        conn_temp.close()

        conexao = psycopg2.connect(database="stardew", **config)
        conexao.autocommit = True
        
        with conexao.cursor() as cursor:
            print("resetando bau...")
            cursor.execute('''
                DROP VIEW IF EXISTS vw_produtos_detalhados CASCADE;
                DROP VIEW IF EXISTS vw_historico_cliente CASCADE;
                DROP TABLE IF EXISTS itens_venda CASCADE;
                DROP TABLE IF EXISTS vendas CASCADE;
                DROP TABLE IF EXISTS vendedores CASCADE;
                DROP TABLE IF EXISTS formas_pagamento CASCADE;
                DROP TABLE IF EXISTS clientes CASCADE;
                DROP TABLE IF EXISTS produtos CASCADE;
                DROP TABLE IF EXISTS categorias CASCADE;
                DROP TABLE IF EXISTS qualidades CASCADE;

                CREATE TABLE categorias (id_categoria SERIAL PRIMARY KEY, nome VARCHAR(255) UNIQUE, valor_base REAL);
                CREATE TABLE qualidades (id_qualidade SERIAL PRIMARY KEY, nome VARCHAR(255) UNIQUE, multiplicador REAL);
                
                CREATE TABLE produtos (
                    id_produto SERIAL PRIMARY KEY, 
                    nome VARCHAR(255), 
                    quantidade_estoque INT, 
                    id_categoria INT REFERENCES categorias, 
                    id_qualidade INT REFERENCES qualidades,
                    fabricado_em_mari BOOLEAN DEFAULT FALSE
                );

                CREATE TABLE clientes (
                    id_cliente SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    torce_flamengo BOOLEAN,
                    assiste_one_piece BOOLEAN,
                    de_sousa_pb BOOLEAN
                );
                
                -- INDICE PARA IGNORAR CASE SENSITIVE NO CADASTRO
                CREATE UNIQUE INDEX idx_cliente_nome_lower ON clientes (LOWER(nome));

                CREATE TABLE vendedores (id_vendedor SERIAL PRIMARY KEY, nome VARCHAR(255));
                CREATE TABLE formas_pagamento (id_forma_pagamento SERIAL PRIMARY KEY, nome VARCHAR(255));

                CREATE TABLE vendas (
                    id_venda SERIAL PRIMARY KEY, id_cliente INT REFERENCES clientes, id_vendedor INT REFERENCES vendedores,
                    id_forma_pagamento INT REFERENCES formas_pagamento, valor_bruto REAL DEFAULT 0,
                    desconto_aplicado REAL DEFAULT 0, valor_liquido REAL DEFAULT 0, data_venda TIMESTAMP DEFAULT NOW()
                );

                CREATE TABLE itens_venda (
                    id_item SERIAL PRIMARY KEY, id_venda INT REFERENCES vendas, id_produto INT REFERENCES produtos,
                    quantidade INT, preco_unitario REAL, subtotal REAL
                );

                -- DADOS
                INSERT INTO categorias (nome, valor_base) VALUES ('Semente', 20.0), ('Cultivo', 80.0), ('Artesanato', 300.0);
                INSERT INTO qualidades (nome, multiplicador) VALUES ('Normal', 1.0), ('Ouro', 1.5), ('Irídio', 2.0);
                INSERT INTO vendedores (nome) VALUES ('Pierre'), ('Abigail');
                INSERT INTO formas_pagamento (nome) VALUES ('Ouro'), ('Débito'), ('Joja Card');
                INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade) VALUES ('Semente de Chirívia', 100, 1, 1);

                -- VIEWS
                CREATE VIEW vw_produtos_detalhados AS
                SELECT p.id_produto, p.nome, (c.valor_base * q.multiplicador) AS preco_venda, c.nome AS categoria, p.quantidade_estoque, p.fabricado_em_mari
                FROM produtos p JOIN categorias c ON p.id_categoria = c.id_categoria JOIN qualidades q ON p.id_qualidade = q.id_qualidade;

                -- VIEW: Histórico detalhado com itens e quantidades
                CREATE VIEW vw_historico_cliente AS
                SELECT v.id_cliente, v.data_venda, v.id_venda, STRING_AGG(p.nome || ' (' || iv.quantidade || 'x)', ', ') AS itens, fp.nome as forma_pagamento, v.valor_bruto, v.valor_liquido
                FROM vendas v
                JOIN itens_venda iv ON v.id_venda = iv.id_venda
                JOIN produtos p ON iv.id_produto = p.id_produto
                JOIN formas_pagamento fp ON v.id_forma_pagamento = fp.id_forma_pagamento
                GROUP BY v.id_venda, v.id_cliente, v.data_venda, fp.nome;

                -- PROCEDURES
                CREATE OR REPLACE PROCEDURE sp_adicionar_item_venda(p_id_venda INT, p_id_produto INT, p_quantidade INT)
                LANGUAGE plpgsql AS $$
                DECLARE v_preco REAL;
                BEGIN
                    SELECT preco_venda INTO v_preco FROM vw_produtos_detalhados WHERE id_produto = p_id_produto;
                    INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario, subtotal)
                    VALUES (p_id_venda, p_id_produto, p_quantidade, v_preco, v_preco * p_quantidade);
                    UPDATE produtos SET quantidade_estoque = quantidade_estoque - p_quantidade WHERE id_produto = p_id_produto;
                    UPDATE vendas SET valor_bruto = valor_bruto + (v_preco * p_quantidade) WHERE id_venda = p_id_venda;
                END;
                $$;

                CREATE OR REPLACE PROCEDURE sp_finalizar_venda(p_id_venda INT)
                LANGUAGE plpgsql AS $$
                DECLARE v_bruto REAL; v_desc_perc INT := 0; v_cli RECORD;
                BEGIN
                    SELECT c.* INTO v_cli FROM vendas v JOIN clientes c ON v.id_cliente = c.id_cliente WHERE v.id_venda = p_id_venda;
                    IF v_cli.torce_flamengo THEN v_desc_perc := v_desc_perc + 10; END IF;
                    IF v_cli.assiste_one_piece THEN v_desc_perc := v_desc_perc + 10; END IF;
                    IF v_cli.de_sousa_pb THEN v_desc_perc := v_desc_perc + 10; END IF;
                    SELECT valor_bruto INTO v_bruto FROM vendas WHERE id_venda = p_id_venda;
                    UPDATE vendas SET desconto_aplicado = v_bruto * (v_desc_perc / 100.0), valor_liquido = v_bruto - (v_bruto * (v_desc_perc / 100.0)) WHERE id_venda = p_id_venda;
                END;
                $$;
            ''')
        print("bau resetado!")
    except Exception as e:
        print(f"erro: {e}")

if __name__ == "__main__":
    resetar_banco()