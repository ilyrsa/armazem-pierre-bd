import psycopg2
import os
from dotenv import load_dotenv

# Carrega as configurações do .env
load_dotenv()

class GerenciadorArmazem:
    def __init__(self):
        try:
            self.conexao = psycopg2.connect(
                host=os.getenv("DB_HOST", "127.0.0.1"),
                database=os.getenv("DB_NAME", "stardew"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASS", "1234"),
                port=os.getenv("DB_PORT", "5432")
            )
            print(f"✅ Conectado ao banco como: {os.getenv('DB_USER')}")
        except Exception as e:
            print(f"❌ Falha ao iniciar Gerenciador: {e}")
            raise

    # --- GESTÃO DE ESTOQUE (NOVO/AJUSTADO) ---

    # Adicionar um produto totalmente novo ao banco
    def adicionar_novo_produto(self, nome, quantidade_estoque, id_categoria, id_qualidade, fabricado_em_mari=False):
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade, fabricado_em_mari)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (nome, quantidade_estoque, id_categoria, id_qualidade, fabricado_em_mari))
                self.conexao.commit()
                return True
        except Exception as e:
            print(f"Erro ao inserir: {e}")
            self.conexao.rollback()
            return False

    # Modificar apenas a quantidade de um produto existente (Ajuste de Estoque)
    def ajustar_estoque(self, id_produto, nova_qtd):
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute("UPDATE produtos SET quantidade_estoque = %s WHERE id_produto = %s", (nova_qtd, id_produto))
                self.conexao.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao ajustar estoque: {e}")
            self.conexao.rollback()
            return False

    # ------------------------------------------

    def alterar_produto(self, id_produto, novo_nome=None, nova_qtd=None):
        campos, valores = [], []
        if novo_nome:
            campos.append("nome = %s"); valores.append(novo_nome)
        if nova_qtd is not None:
            campos.append("quantidade_estoque = %s"); valores.append(nova_qtd)
        
        if not campos: return False
        valores.append(id_produto)

        with self.conexao.cursor() as cursor:
            cursor.execute(f"UPDATE produtos SET {', '.join(campos)} WHERE id_produto = %s", tuple(valores))
            self.conexao.commit()
            return cursor.rowcount > 0

    def pesquisar_por_nome(self, nome_pesquisa):
        with self.conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos WHERE nome ILIKE %s", (f'%{nome_pesquisa}%',))
            return cursor.fetchall()

    def remover_produto(self, id_produto):
        with self.conexao.cursor() as cursor:
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
            self.conexao.commit()
            return cursor.rowcount > 0

    def listar_todos(self):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT p.id_produto, p.nome, p.quantidade_estoque, c.nome, q.nome
                FROM produtos p
                JOIN categorias c ON p.id_categoria = c.id_categoria
                JOIN qualidades q ON p.id_qualidade = q.id_qualidade
                ORDER BY p.id_produto ASC
            ''')
            return cursor.fetchall()

    def exibir_um(self, id_produto):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT p.nome, p.quantidade_estoque, c.nome, q.nome, c.valor_base, q.multiplicador
                FROM produtos p
                JOIN categorias c ON p.id_categoria = c.id_categoria
                JOIN qualidades q ON p.id_qualidade = q.id_qualidade
                WHERE p.id_produto = %s
            ''', (id_produto,))
            res = cursor.fetchone()
            if res:
                return {
                    "nome": res[0], "estoque": res[1], "categoria": res[2],
                    "qualidade": res[3], "valor_unitario": res[4] * res[5]
                }
            return None

    def gerar_relatorio(self):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT p.quantidade_estoque, c.valor_base, q.multiplicador, c.nome
                FROM produtos p
                JOIN categorias c ON p.id_categoria = c.id_categoria
                JOIN qualidades q ON p.id_qualidade = q.id_qualidade
            ''')
            itens = cursor.fetchall()
            
            tipos = len(itens)
            total_un = sum(i[0] for i in itens)
            valor_total = sum(i[0] * (i[1] * i[2]) for i in itens)
            
            por_cat = {}
            for i in itens:
                por_cat[i[3]] = por_cat.get(i[3], 0) + i[0]
            
            return tipos, total_un, valor_total, por_cat

    def listar_catalogo_filtrado(self, nome=None, preco_min=None, preco_max=None, categoria=None, mari=None):
        query = "SELECT * FROM vw_produtos_detalhados WHERE 1=1"
        params = []
        if nome: query += " AND nome ILIKE %s"; params.append(f'%{nome}%')
        if preco_min: query += " AND preco_venda >= %s"; params.append(preco_min)
        if preco_max: query += " AND preco_venda <= %s"; params.append(preco_max)
        if categoria: query += " AND categoria ILIKE %s"; params.append(f'%{categoria}%')
        if mari is not None: query += " AND fabricado_em_mari = %s"; params.append(mari)
        
        with self.conexao.cursor() as cursor:
            cursor.execute(query + " ORDER BY id_produto ASC", tuple(params))
            return cursor.fetchall()

    def registrar_cliente(self, nome, fla, op, sousa):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                INSERT INTO clientes (nome, torce_flamengo, assiste_one_piece, de_sousa_pb)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (LOWER(nome)) DO UPDATE SET nome = EXCLUDED.nome
                RETURNING id_cliente
            ''', (nome, fla, op, sousa))
            self.conexao.commit()
            return cursor.fetchone()[0]

    def listar_opcoes(self, tabela):
        mapeamento = {
            'vendedores': "SELECT id_vendedor, nome FROM vendedores",
            'formas_pagamento': "SELECT id_forma_pagamento, nome FROM formas_pagamento",
            'categorias': "SELECT id_categoria, nome, valor_base FROM categorias",
            'qualidades': "SELECT id_qualidade, nome, multiplicador FROM qualidades"
        }
        with self.conexao.cursor() as cursor:
            cursor.execute(mapeamento.get(tabela, "SELECT 1") + " ORDER BY 1")
            return cursor.fetchall()

    def processar_venda_completa(self, id_cliente, id_vendedor, id_forma_pagamento, carrinho):
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO vendas (id_cliente, id_vendedor, id_forma_pagamento)
                    VALUES (%s, %s, %s) RETURNING id_venda
                ''', (id_cliente, id_vendedor, id_forma_pagamento))
                id_venda = cursor.fetchone()[0]

                for item in carrinho:
                    cursor.execute("CALL sp_adicionar_item_venda(%s, %s, %s)", (id_venda, item['id_prod'], item['qtd']))

                cursor.execute("CALL sp_finalizar_venda(%s)", (id_venda,))
                cursor.execute("SELECT valor_bruto, desconto_aplicado, valor_liquido FROM vendas WHERE id_venda = %s", (id_venda,))
                res = cursor.fetchone()
                self.conexao.commit()
                return True, res
        except Exception as e:
            self.conexao.rollback()
            return False, str(e)

    def historico_pedidos_cliente(self, id_cliente):
        with self.conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM vw_historico_cliente WHERE id_cliente = %s ORDER BY data_venda DESC", (id_cliente,))
            return cursor.fetchall()

    def filtrar_estoque_baixo(self):
        with self.conexao.cursor() as cursor:
            cursor.execute("SELECT id_produto, nome, quantidade_estoque FROM produtos WHERE quantidade_estoque < 5")
            return cursor.fetchall()

    def relatorio_vendas_mensal(self, mes, ano):
        with self.conexao.cursor() as cursor:
            cursor.execute("SELECT vendedor, total_vendas, total_arrecadado FROM vw_relatorio_vendas_mensal WHERE mes = %s AND ano = %s", (mes, ano))
            return cursor.fetchall()

    def listar_clientes(self):
        with self.conexao.cursor() as cursor:
            cursor.execute("SELECT id_cliente, nome, torce_flamengo, assiste_one_piece, de_sousa_pb FROM clientes")
            return cursor.fetchall()

    def fechar_conexao(self):
        if self.conexao: self.conexao.close()