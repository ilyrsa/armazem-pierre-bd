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

    # Limpeza total antes de recriar o banco de dados
    cursor.execute('''
    DROP TABLE IF EXISTS produtos CASCADE;
    DROP TABLE IF EXISTS categorias CASCADE;
    DROP TABLE IF EXISTS qualidades CASCADE;
    ''')

    # 1. Categorias e qualidades dos produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria SERIAL PRIMARY KEY,
        nome         VARCHAR(255) UNIQUE NOT NULL,
        valor_base   REAL NOT NULL    
    );

    CREATE TABLE qualidades (
        id_qualidade   SERIAL PRIMARY KEY,
        nome           VARCHAR(255) UNIQUE NOT NULL,
        multiplicador  REAL NOT NULL        -- ex: Irídio = 2.0 → dobra o preço base
    );
    ''')

    # Entidade auxiliar para qualidades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS qualidades (
        id_qualidade SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL UNIQUE,
        multiplicador REAL NOT NULL   
    );
    ''')

    # Objeto principal: produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id_produto SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        quantidade_estoque INTEGER NOT NULL,
        id_categoria INTEGER NOT NULL,
        id_qualidade INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
        FOREIGN KEY (id_qualidade) REFERENCES qualidades(id_qualidade)
    );
    ''')

    # Inserindo dados iniciais
    cursor.execute('''
        INSERT INTO categorias (nome, valor_base) VALUES
        ('Semente',   20.0),   -- 1: sementes para plantar na fazenda
        ('Cultivo',   80.0),   -- 2: vegetais já colhidos
        ('Coleta',    50.0),   -- 3: itens coletados na natureza
        ('Peixe',    100.0),   -- 4: peixes do rio, lago e oceano
        ('Muda',     800.0),   -- 5: mudas de árvores frutíferas
        ('Culinária',100.0),   -- 6: ingredientes para receitas
        ('Artesanato',300.0)   -- 7: produtos processados em máquinas
    ''')

    # Qualidades do sistema 
    cursor.execute('''
        INSERT INTO qualidades (nome, multiplicador) VALUES
        ('Normal', 1.00),   -- qualidade padrão, sem bônus
        ('Prata',  1.25),   -- +25% de valor
        ('Ouro',   1.50),   -- +50% de valor
        ('Irídio', 2.00)    -- dobro do valor base (máximo de qualidade)
    ''')

    # População inicial de produtos
    cursor.execute('''
        INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade, fabricado_em_mari)
        VALUES
        -- Sementes (Cat 1)
        ('Semente de Chirívia', 500, 1, 1, FALSE),
        ('Semente de Batata',   200, 1, 1, FALSE),
        ('Semente de Couve',    100, 1, 1, FALSE),
        
        -- Cultivos (Cat 2)
        ('Chirívia',            20,  2, 1, FALSE),
        ('Batata',              15,  2, 2, FALSE), 
        ('Couve',               10,  2, 3, FALSE),  
        
        -- Coleta (Cat 3)
        ('Amora',               3,   3, 2, TRUE),   
        ('Raiz de Inverno',     5,   3, 1, FALSE),
        ('Inhame de Neve',      8,   3, 4, FALSE),  
        
        -- Peixes (Cat 4)
        ('Peixe Lenda',         1,   4, 4, FALSE),  
        ('Robalo',              5,   4, 1, FALSE),
        ('Truta',               4,   4, 2, FALSE),
        
        -- Mudas (Cat 5)
        ('Muda de Cerejeira',   10,  5, 1, FALSE),
        ('Muda de Macieira',    10,  5, 1, FALSE),
        ('Muda de Pessegueiro', 10,  5, 1, FALSE),
        
        -- Culinária (Cat 6)
        ('Farinha de Trigo',    50,  6, 1, FALSE),
        ('Açúcar',              50,  6, 1, FALSE),
        ('Óleo',                50,  6, 1, FALSE),
        
        -- Artesanato (Cat 7)
        ('Maionese',            20,  7, 3, FALSE),  
        ('Vinho de Carambola',  15,  7, 4, FALSE),  
        ('Geleia de Mirtilo',   25,  7, 2, FALSE)   
    ''')

    print("✅ Baú do Pierre resetado! Tabelas, Views e Procedures de Venda criadas com sucesso!")

except Exception as e:
    print(f"Erro ao conectar ou criar o banco: {e}")