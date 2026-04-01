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
            print(f" Conectado ao banco como: {os.getenv('DB_USER')}")
        except Exception as e:
            print(f" Falha ao iniciar Gerenciador: {e}")
            raise

    # 1. Inserir produto
    def inserir_produto(self, nome, quantidade_estoque, id_categoria, id_qualidade, fabricado_em_mari=False):
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

    # 2. Alterar nome e/ou quantidade de estoque de um produto pelo id
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

        with self.conexao.cursor() as cursor:
            cursor.execute(f'''
                UPDATE produtos
                SET {", ".join(campos)}
                WHERE id_produto = %s
                ''', tuple(valores))
        self.conexao.commit()
        return cursor.rowcount > 0

    # 3. Pesquisar por nome 
    def pesquisar_por_nome(self, nome_pesquisa):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM produtos WHERE nome ILIKE %s
            ''', (f'%{nome_pesquisa}%',))
            return cursor.fetchall()

    # 4. Remover produto pelo id
    def remover_produto(self, id_produto):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                DELETE FROM produtos WHERE id_produto = %s
            ''', (id_produto,))
        self.conexao.commit()
        return cursor.rowcount > 0
    
    # 5. Listar todos os produtos com categoria e qualidade
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

    # 6. Exibir um produto detalhado com o preço final calculado
    def exibir_um(self, id_produto):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT p.nome, p.quantidade_estoque, c.nome, q.nome, c.valor_base, q.multiplicador
                FROM produtos p
                JOIN categorias c ON p.id_categoria = c.id_categoria
                JOIN qualidades q ON p.id_qualidade = q.id_qualidade
                WHERE p.id_produto = %s
            ''', (id_produto,))
            produto = cursor.fetchone()

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

    # 7. Relatório geral do estoque
    def gerar_relatorio(self):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT p.quantidade_estoque, c.valor_base, q.multiplicador, c.nome
                FROM produtos p
                JOIN categorias c ON p.id_categoria = c.id_categoria
                JOIN qualidades q ON p.id_qualidade = q.id_qualidade
            ''')
            itens = cursor.fetchall()

        tipos_produtos = len(itens)
        total_elementos = 0
        valor_total_estoque = 0.0
        qtd_por_categoria = {}

        for estoque, valor_base, multiplicador, categoria in itens:
            total_elementos += estoque
            valor_total_estoque += (estoque * (valor_base * multiplicador))

            if categoria in qtd_por_categoria:
                qtd_por_categoria[categoria] += estoque
            else:
                qtd_por_categoria[categoria] = estoque

        return tipos_produtos, total_elementos, valor_total_estoque, qtd_por_categoria
    
    # 8. Listar catálogo com filtros dinâmicos opcionais
    def listar_catalogo_filtrado(self, nome=None, preco_min=None, preco_max=None, categoria=None, mari=None):
        condicoes = []
        valores = []

        # Filtra por trecho do nome
        if nome:
            condicoes.append("nome ILIKE %s")
            valores.append(f'%{nome}%')

        # Filtra pela faixa de preço calculada
        if preco_min is not None:
            condicoes.append("preco_venda >= %s")
            valores.append(preco_min)
        if preco_max is not None:
            condicoes.append("preco_venda <= %s")
            valores.append(preco_max)

        # Filtra por nome de categoria
        if categoria:
            condicoes.append("categoria ILIKE %s")
            valores.append(f'%{categoria}%')

        # Filtra por origem (fabricado em Mari-PB ou não)
        if mari is not None:
            condicoes.append("fabricado_em_mari = %s")
            valores.append(mari)

        where = ("WHERE " + " AND ".join(condicoes)) if condicoes else ""

        with self.conexao.cursor() as cursor:
            cursor.execute(f'''
                SELECT id_produto, nome, preco_venda, categoria, quantidade_estoque, fabricado_em_mari
                FROM vw_produtos_detalhados
                {where}
                ORDER BY id_produto ASC
            ''', tuple(valores))
            return cursor.fetchall()

    # 9. Registrar um cliente pelo nome
    def registrar_cliente(self, nome, torce_flamengo, assiste_one_piece, de_sousa_pb):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                INSERT INTO clientes (nome, torce_flamengo, assiste_one_piece, de_sousa_pb)
                VALUES (%s, %s, %s, %s)
                RETURNING id_cliente
            ''', (nome, torce_flamengo, assiste_one_piece, de_sousa_pb))
            id_cliente = cursor.fetchone()[0]
        self.conexao.commit()
        return id_cliente

    # 10. Listar opções de uma tabela auxiliar para popular menus de escolha
    def listar_opcoes(self, tabela):
        with self.conexao.cursor() as cursor:
            if tabela == 'vendedores':
                cursor.execute("SELECT id_vendedor, nome FROM vendedores ORDER BY id_vendedor")
            elif tabela == 'formas_pagamento':
                cursor.execute("SELECT id_forma_pagamento, nome FROM formas_pagamento ORDER BY id_forma_pagamento")
            elif tabela == 'categorias':
                cursor.execute("SELECT id_categoria, nome, valor_base FROM categorias ORDER BY id_categoria")
            elif tabela == 'qualidades':
                cursor.execute("SELECT id_qualidade, nome, multiplicador FROM qualidades ORDER BY id_qualidade")
            else:
                return []
            return cursor.fetchall()

    # 11. Processar uma venda completa do início ao fim
    def processar_venda_completa(self, id_cliente, id_vendedor, id_forma_pagamento, carrinho):
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO vendas (id_cliente, id_vendedor, id_forma_pagamento)
                    VALUES (%s, %s, %s)
                    RETURNING id_venda
                ''', (id_cliente, id_vendedor, id_forma_pagamento))
                id_venda = cursor.fetchone()[0]

            with self.conexao.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO vendas (id_cliente, id_vendedor, id_forma_pagamento)
                    VALUES (%s, %s, %s)
                    RETURNING id_venda
                ''', (id_cliente, id_vendedor, id_forma_pagamento))
                id_venda = cursor.fetchone()[0]

                for item in carrinho:
                    cursor.execute(
                        "CALL sp_adicionar_item_venda(%s, %s, %s)",
                        (id_venda, item['id_prod'], item['qtd'])
                    )

                cursor.execute("CALL sp_finalizar_venda(%s)", (id_venda,))
                cursor.execute('''
                    SELECT valor_bruto, desconto_aplicado, valor_liquido
                    FROM vendas WHERE id_venda = %s
                ''', (id_venda,))
                bruto, desconto, liquido = cursor.fetchone()

            self.conexao.commit()
            return True, (bruto, desconto, liquido) 
        except Exception as e:
            self.conexao.rollback()
            return False, str(e)

    # 12. Histórico de pedidos de um cliente específico (usa a view vw_historico_cliente)
    def historico_pedidos_cliente(self, id_cliente):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT id_venda, data_venda, forma_pagamento, status_pagamento,
                       valor_bruto, desconto_aplicado, valor_liquido
                FROM vw_historico_cliente
                WHERE id_cliente = %s
                ORDER BY data_venda DESC
            ''', (id_cliente,))
            return cursor.fetchall()

    # 13. Filtrar produtos com estoque crítico (menos de 5 unidades)
    def filtrar_estoque_baixo(self):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT id_produto, nome, quantidade_estoque
                FROM produtos
                WHERE quantidade_estoque < 5
                ORDER BY quantidade_estoque ASC
            ''')
            return cursor.fetchall()

    # 14. Relatório mensal de vendas por vendedor
    def relatorio_vendas_mensal(self, mes, ano):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT vendedor, total_vendas, total_arrecadado
                FROM vw_relatorio_vendas_mensal
                WHERE mes = %s AND ano = %s
                ORDER BY total_arrecadado DESC
            ''', (mes, ano))
            return cursor.fetchall()
        
    # 15. Listar os clientes que tem
    def listar_clientes(self):
        with self.conexao.cursor() as cursor:
            cursor.execute('''
                SELECT id_cliente, nome, torce_flamengo, assiste_one_piece, de_sousa_pb
                FROM clientes
                ORDER BY id_cliente ASC
            ''')
            return cursor.fetchall()

    def fechar_conexao(self):
        if self.conexao:
            self.conexao.close()