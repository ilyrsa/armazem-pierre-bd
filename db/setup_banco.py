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

    # Limpa o banco antes de criar um novo
    cursor.execute('''
    DROP TABLE IF EXISTS produtos CASCADE;
    DROP TABLE IF EXISTS categorias CASCADE;
    DROP TABLE IF EXISTS qualidades CASCADE;
    ''')

    # Criando as tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL UNIQUE,
        valor_base REAL NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS qualidades (
        id_qualidade SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL UNIQUE,
        multiplicador REAL NOT NULL   
    );
    ''')

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
        ('Semente', 20.0),
        ('Cultivo (Frutas/Hortaliças)', 80.0),
        ('Coleta', 50.0),
        ('Peixe', 100.0),
        ('Produto Artesanal', 300.0)
        ON CONFLICT (nome) DO NOTHING;

        INSERT INTO qualidades (nome, multiplicador) VALUES 
        ('Normal', 1.0),
        ('Prata', 1.25),
        ('Ouro', 1.5),
        ('Irídio', 2.0)
        ON CONFLICT (nome) DO NOTHING;
    ''')

    # População inicial de produtos
    cursor.execute('''
        INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade) VALUES
        ('Vinho de Carambola', 15, 5, 4),   
        ('Semente de Chuva', 50, 1, 1),    
        ('Melão', 20, 2, 3),                 
        ('Amora', 35, 3, 2),                 
        ('Peixe Lenda', 1, 4, 4),
        ('Óleo de Trufas', 12, 5, 4);          
    ''')

    cursor.close()
    conexao.close()
    print("Baú do Stardew Valley resetado e populado com sucesso!")

except Exception as e:
    print(f"Erro ao conectar ou criar o banco: {e}")