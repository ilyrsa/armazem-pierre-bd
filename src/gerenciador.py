import psycopg2

class GerenciadorArmazem:
    def __init__(self):
        # Conecta ao servidor local
        self.conexao = psycopg2.connect(
            host="localhost",
            database="stardew",
            user="lari",
            password="1234"
        )
        self.cursor = self.conexao.cursor()

    # 1. Inserir
    def inserir_produto(self, nome, quantidade_estoque, id_categoria, id_qualidade):
        try:
            self.cursor.execute('''
                INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade)
                VALUES (%s, %s, %s, %s)
            ''', (nome, quantidade_estoque, id_categoria, id_qualidade))
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir: {e}")
            self.conexao.rollback()
            return False

    # 2. Alterar
    def alterar_produto(self, id_produto, novo_nome=None, nova_qtd=None):
        if novo_nome is None and nova_qtd is None:
            print("Nenhum campo informado para alterar.")
            return False

        campos = []
        valores = []

        if novo_nome is not None:
            campos.append("nome = %s")
            valores.append(novo_nome)

        if nova_qtd is not None:
            campos.append("quantidade_estoque = %s")
            valores.append(nova_qtd)

        valores.append(id_produto)

        self.cursor.execute(f'''
            UPDATE produtos
            SET {", ".join(campos)}
            WHERE id_produto = %s
            ''', tuple(valores))

        self.conexao.commit()
        return self.cursor.rowcount > 0

    # 3. Pesquisar por nome
    def pesquisar_por_nome(self, nome_pesquisa):
        self.cursor.execute('''
            SELECT * FROM produtos WHERE nome ILIKE %s
        ''', (f'%{nome_pesquisa}%',)) 
        return self.cursor.fetchall()

    # 4. Remover
    def remover_produto(self, id_produto):
        self.cursor.execute('''
            DELETE FROM produtos WHERE id_produto = %s
        ''', (id_produto,))
        self.conexao.commit()
        return self.cursor.rowcount > 0

    # 5. Listar todos
    def listar_todos(self):
        self.cursor.execute('''
            SELECT p.id_produto, p.nome, p.quantidade_estoque, c.nome, q.nome 
            FROM produtos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN qualidades q ON p.id_qualidade = q.id_qualidade
            ORDER BY p.id_produto ASC
        ''')
        return self.cursor.fetchall()

    # 6. Exibir um e calcular preço total
    def exibir_um(self, id_produto):
        self.cursor.execute('''
            SELECT p.nome, p.quantidade_estoque, c.nome, q.nome, c.valor_base, q.multiplicador
            FROM produtos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN qualidades q ON p.id_qualidade = q.id_qualidade
            WHERE p.id_produto = %s
        ''', (id_produto,))
        produto = self.cursor.fetchone()
        
        if produto:
            nome, qtd, cat, qual, valor_base, multiplicador = produto
            valor_final = valor_base * multiplicador 
            return {
                "nome": nome,
                "estoque": qtd,
                "categoria": cat,
                "qualidade": qual,
                "valor_unitario": valor_final
            }
        return None

    # 7. Relatório 
    def gerar_relatorio(self):
        self.cursor.execute('''
            SELECT p.quantidade_estoque, c.valor_base, q.multiplicador
            FROM produtos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN qualidades q ON p.id_qualidade = q.id_qualidade
        ''')
        itens = self.cursor.fetchall()
        
        tipos_produtos = len(itens) 
        total_elementos = 0
        valor_total_estoque = 0.0
        
        for estoque, valor_base, multiplicador in itens:
            total_elementos += estoque
            valor_total_estoque += (estoque * (valor_base * multiplicador))
            
        return tipos_produtos, total_elementos, valor_total_estoque

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()