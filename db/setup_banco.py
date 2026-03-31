import psycopg2

try:
    # Conectando ao servidor do PostgreSQL
    conexao = psycopg2.connect(
        host="localhost",
        database="stardew",
        user="lari",
        password="1234"
    )
    conexao.autocommit = True
    cursor = conexao.cursor()

    # Limpeza completa antes de recriar as tabelas
    cursor.execute('''
        DROP VIEW IF EXISTS vw_produtos_detalhados CASCADE;
        DROP VIEW IF EXISTS vw_historico_cliente CASCADE;
        DROP VIEW IF EXISTS vw_relatorio_vendas_mensal CASCADE;
        DROP TABLE IF EXISTS itens_venda CASCADE;
        DROP TABLE IF EXISTS vendas CASCADE;
        DROP TABLE IF EXISTS vendedores CASCADE;
        DROP TABLE IF EXISTS formas_pagamento CASCADE;
        DROP TABLE IF EXISTS clientes CASCADE;
        DROP TABLE IF EXISTS produtos CASCADE;
        DROP TABLE IF EXISTS categorias CASCADE;
        DROP TABLE IF EXISTS qualidades CASCADE;
    ''')

    # 1. Categorias e qualidades dos produtos
    cursor.execute('''
        CREATE TABLE categorias (
            id_categoria SERIAL PRIMARY KEY,
            nome VARCHAR(255) UNIQUE NOT NULL,
            valor_base REAL NOT NULL
        );

        CREATE TABLE qualidades (
            id_qualidade SERIAL PRIMARY KEY,
            nome VARCHAR(255) UNIQUE NOT NULL,
            multiplicador REAL NOT NULL
        );
    ''')

    # Produtos disponíveis para venda
    cursor.execute('''
        CREATE TABLE produtos (
            id_produto SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            quantidade_estoque INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL REFERENCES categorias(id_categoria),
            id_qualidade INTEGER NOT NULL REFERENCES qualidades(id_qualidade),
            fabricado_em_mari BOOLEAN DEFAULT FALSE
        );
    ''')

    # Clientes e Vendedores
    cursor.execute('''
        CREATE TABLE clientes (
            id_cliente SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            torce_flamengo BOOLEAN DEFAULT FALSE,
            assiste_one_piece BOOLEAN DEFAULT FALSE,
            de_sousa_pb BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE vendedores (
            id_vendedor SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL
        );
    ''')

    # Formas de pagamento
    cursor.execute('''
        CREATE TABLE formas_pagamento (
            id_forma_pagamento SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL
        );
    ''')       

    # Vendas e itens vendidos
    cursor.execute(''' 
        CREATE TABLE vendas (
            id_venda SERIAL PRIMARY KEY,
            id_cliente INTEGER REFERENCES clientes(id_cliente),
            id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
            id_forma_pagamento INTEGER REFERENCES formas_pagamento(id_forma_pagamento),
            data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status_pagamento VARCHAR(50) DEFAULT 'Pendente',
            valor_bruto REAL DEFAULT 0,
            desconto_aplicado REAL DEFAULT 0,
            valor_liquido REAL DEFAULT 0
        );

        CREATE TABLE itens_venda (
            id_item SERIAL PRIMARY KEY,
            id_venda INTEGER REFERENCES vendas(id_venda),
            id_produto INTEGER REFERENCES produtos(id_produto),
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            subtotal REAL NOT NULL
        );
    ''')

    # Inserindo dados iniciais
    cursor.execute('''
        INSERT INTO categorias (nome, valor_base) VALUES
        ('Semente', 20.0), ('Cultivo', 80.0), ('Coleta', 50.0),
        ('Peixe', 100.0), ('Muda', 800.0), ('Culinária', 100.0), ('Artesanato', 300.0);

        INSERT INTO qualidades (nome, multiplicador) VALUES
        ('Normal', 1.00), ('Prata', 1.25), ('Ouro', 1.50), ('Irídio', 2.00);

        INSERT INTO vendedores (nome) VALUES 
        ('Pierre'), ('Abigail');

        INSERT INTO formas_pagamento (nome) VALUES 
        ('Ouro (Dinheiro)'), ('Cartão de Débito'), ('Vale do Prefeito');

        INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade, fabricado_em_mari) VALUES
        ('Semente de Chirívia', 500, 1, 1, FALSE), ('Semente de Batata', 200, 1, 1, FALSE),
        ('Semente de Couve', 100, 1, 1, FALSE), ('Chirívia', 20, 2, 1, FALSE),
        ('Batata', 15, 2, 2, FALSE), ('Couve', 10, 2, 3, FALSE),
        ('Amora', 3, 3, 2, TRUE), ('Raiz de Inverno', 5, 3, 1, FALSE),
        ('Inhame de Neve', 8, 3, 4, FALSE), ('Peixe Lenda', 1, 4, 4, FALSE),
        ('Robalo', 5, 4, 1, FALSE), ('Truta', 4, 4, 2, FALSE),
        ('Muda de Cerejeira', 10, 5, 1, FALSE), ('Muda de Macieira', 10, 5, 1, FALSE),
        ('Muda de Pessegueiro', 10, 5, 1, FALSE), ('Farinha de Trigo', 50, 6, 1, FALSE),
        ('Açúcar', 50, 6, 1, FALSE), ('Óleo', 50, 6, 1, FALSE),
        ('Maionese', 20, 7, 3, FALSE), ('Vinho de Carambola', 15, 7, 4, FALSE),
        ('Geleia de Mirtilo', 25, 7, 2, FALSE);
                   
        INSERT INTO clientes (nome, torce_flamengo, assiste_one_piece, de_sousa_pb) VALUES
        ('Prefeito Lewis', FALSE, FALSE, FALSE),
        ('Robin', FALSE, TRUE, FALSE),
        ('Marnie', FALSE, FALSE, FALSE),
        ('Willy', FALSE, FALSE, FALSE),
        ('Pam', TRUE, FALSE, FALSE),
        ('Gus', TRUE, TRUE, TRUE),
        ('Clint', FALSE, FALSE, FALSE);
                   
        INSERT INTO vendas (id_cliente, id_vendedor, id_forma_pagamento, data_venda, status_pagamento, valor_bruto, desconto_aplicado, valor_liquido) VALUES
        -- MÊS 1: JANEIRO 2026 (4 Vendas)
        (3, 1, 1, '2026-01-05 10:30:00', 'Confirmado', 500.0, 0, 500.0),     
        (4, 2, 2, '2026-01-12 14:15:00', 'Confirmado', 1200.0, 0, 1200.0),    
        (5, 1, 1, '2026-01-18 16:45:00', 'Confirmado', 300.0, 30.0, 270.0),  
        (6, 2, 3, '2026-01-25 09:00:00', 'Confirmado', 150.0, 0, 150.0),

        -- MÊS 2: FEVEREIRO 2026 (3 Vendas)
        (7, 1, 1, '2026-02-03 11:20:00', 'Confirmado', 450.0, 0, 450.0),  
        (3, 2, 2, '2026-02-14 13:00:00', 'Confirmado', 800.0, 0, 800.0),    
        (4, 1, 1, '2026-02-28 17:10:00', 'Confirmado', 950.0, 0, 950.0),    
    
        -- MÊS 3: MARÇO 2026 (3 Vendas)
        (5, 1, 2, '2026-03-02 08:45:00', 'Confirmado', 200.0, 20.0, 180.0),  
        (2, 2, 1, '2026-03-10 15:30:00', 'Confirmado', 3000.0, 300.0, 2700.0),
        (1, 1, 3, '2026-03-20 12:00:00', 'Confirmado', 1500.0, 0, 1500.0);
                   
     ''')

    # Criação de Views 
    cursor.execute('''
        CREATE VIEW vw_produtos_detalhados AS
        SELECT p.id_produto, p.nome, (c.valor_base * q.multiplicador) AS preco_venda, 
               c.nome AS categoria, p.quantidade_estoque, p.fabricado_em_mari
        FROM produtos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        JOIN qualidades q ON p.id_qualidade = q.id_qualidade;

        CREATE VIEW vw_historico_cliente AS
        SELECT v.id_venda, v.id_cliente, v.data_venda, f.nome AS forma_pagamento, 
               v.status_pagamento, v.valor_bruto, v.desconto_aplicado, v.valor_liquido
        FROM vendas v
        JOIN formas_pagamento f ON v.id_forma_pagamento = f.id_forma_pagamento;

        CREATE VIEW vw_relatorio_vendas_mensal AS
        SELECT vd.nome AS vendedor, EXTRACT(MONTH FROM v.data_venda) AS mes, 
               EXTRACT(YEAR FROM v.data_venda) AS ano, COUNT(v.id_venda) AS total_vendas, 
               SUM(v.valor_liquido) AS total_arrecadado
        FROM vendas v
        JOIN vendedores vd ON v.id_vendedor = vd.id_vendedor
        WHERE v.status_pagamento = 'Confirmado'
        GROUP BY vd.nome, mes, ano;
    ''')

    # Criação de Procedures 
    cursor.execute('''
        CREATE OR REPLACE PROCEDURE sp_adicionar_item_venda(p_id_venda INT, p_id_produto INT, p_quantidade INT)
        LANGUAGE plpgsql AS $$
        DECLARE
            v_estoque INT;
            v_preco REAL;
            v_subtotal REAL;
        BEGIN
            SELECT quantidade_estoque INTO v_estoque FROM produtos WHERE id_produto = p_id_produto;
            IF v_estoque < p_quantidade THEN
                RAISE EXCEPTION 'Estoque insuficiente para o produto %', p_id_produto;
            END IF;

            SELECT preco_venda INTO v_preco FROM vw_produtos_detalhados WHERE id_produto = p_id_produto;
            v_subtotal := v_preco * p_quantidade;

            INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario, subtotal)
            VALUES (p_id_venda, p_id_produto, p_quantidade, v_preco, v_subtotal);

            UPDATE produtos SET quantidade_estoque = quantidade_estoque - p_quantidade WHERE id_produto = p_id_produto;
            UPDATE vendas SET valor_bruto = valor_bruto + v_subtotal WHERE id_venda = p_id_venda;
        END;
        $$;

        CREATE OR REPLACE PROCEDURE sp_finalizar_venda(p_id_venda INT)
        LANGUAGE plpgsql AS $$
        DECLARE
            v_cliente RECORD;
            v_bruto REAL;
            v_desconto_perc INT := 0;
            v_desconto_valor REAL;
        BEGIN
            SELECT c.torce_flamengo, c.assiste_one_piece, c.de_sousa_pb INTO v_cliente
            FROM vendas v JOIN clientes c ON v.id_cliente = c.id_cliente WHERE v.id_venda = p_id_venda;

            IF v_cliente.torce_flamengo THEN v_desconto_perc := v_desconto_perc + 10; END IF;
            IF v_cliente.assiste_one_piece THEN v_desconto_perc := v_desconto_perc + 10; END IF;
            IF v_cliente.de_sousa_pb THEN v_desconto_perc := v_desconto_perc + 10; END IF;

            SELECT valor_bruto INTO v_bruto FROM vendas WHERE id_venda = p_id_venda;
            v_desconto_valor := v_bruto * (v_desconto_perc / 100.0);

            UPDATE vendas
            SET desconto_aplicado = v_desconto_valor,
                valor_liquido = v_bruto - v_desconto_valor,
                status_pagamento = 'Confirmado'
            WHERE id_venda = p_id_venda;
        END;
        $$;
    ''')

    print("Baú do Pierre resetado! Tabelas, Views e Procedures de Venda criadas com sucesso!")

except Exception as e:
    print(f"Erro ao conectar ou criar o banco: {e}")