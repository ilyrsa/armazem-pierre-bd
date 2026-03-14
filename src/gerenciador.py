import sqlite3
import os

# Caminho para o arquivo do banco de dados
# A classe implementa a lógica de acesso ao banco, e é usada pelo main.py para realizar as operações solicitadas pelo usuário
class GerenciadorArmazem:
    def __init__(self):
        caminho_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'banco.db')
        self.conexao = sqlite3.connect(caminho_db)
        self.cursor = self.conexao.cursor()

    # 1. Inserir
    def inserir_produto(self, nome, quantidade_estoque, id_categoria, id_qualidade):
        try:
            self.cursor.execute('''
                INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade)
                VALUES (?, ?, ?, ?) # O '?' é um placeholder para evitar SQL Injection, 
                                    # e os valores são passados como uma tupla no segundo argumento do execute    
            ''', (nome, quantidade_estoque, id_categoria, id_qualidade))
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir: {e}")
            return False

    # 2. Alterar
    def alterar_produto(self, id_produto, novo_nome, nova_qtd):
        self.cursor.execute('''
            UPDATE produtos
            SET nome = ?, quantidade_estoque = ?
            WHERE id_produto = ?
        ''', (novo_nome, nova_qtd, id_produto))
        self.conexao.commit()

        # O rowcount retorna o número de linhas afetadas pela última operação. Se for maior que 0, significa que a atualização foi bem-sucedida.
        return self.cursor.rowcount > 0

    # 3. Pesquisar por nome
    def pesquisar_por_nome(self, nome_pesquisa):
        # O '%' permite achar partes do nome 
        self.cursor.execute('''
            SELECT * FROM produtos WHERE nome LIKE ?
        ''', (f'%{nome_pesquisa}%',))
        return self.cursor.fetchall()

    # 4. Remover
    def remover_produto(self, id_produto):
        self.cursor.execute('''
            DELETE FROM produtos WHERE id_produto = ?
        ''', (id_produto,))
        self.conexao.commit()
        return self.cursor.rowcount > 0

    # 5. Listar todos
    def listar_todos(self):
        # Fazemos um JOIN para pegar os nomes da categoria e qualidade, e não só os IDs numéricos [cite: 344, 356, 358]
        self.cursor.execute('''
            SELECT p.id_produto, p.nome, p.quantidade_estoque, c.nome, q.nome 
            FROM produtos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN qualidades q ON p.id_qualidade = q.id_qualidade
        ''')
        return self.cursor.fetchall()

    # 6. Exibir um e calcular preço total
    def exibir_um(self, id_produto):
        self.cursor.execute('''
            SELECT p.nome, p.quantidade_estoque, c.nome, q.nome, c.valor_base, q.multiplicador
            FROM produtos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN qualidades q ON p.id_qualidade = q.id_qualidade
            WHERE p.id_produto = ?
        ''', (id_produto,))
        produto = self.cursor.fetchone()
        
        if produto:
            nome, qtd, cat, qual, valor_base, multiplicador = produto
            valor_final = valor_base * multiplicador # A mágica do Stardew Valley aqui!
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
        
        total_elementos = 0
        valor_total_estoque = 0.0
        
        for estoque, valor_base, multiplicador in itens:
            total_elementos += estoque
            valor_total_estoque += (estoque * (valor_base * multiplicador))
            
        return total_elementos, valor_total_estoque

        # Fechar conexão quando o gerenciador for destruído
        def fechar_conexao(self):
            self.conexao.close()
