import sys
import os
from time import sleep


sys.path.append(os.path.dirname(__file__))
from gerenciador import GerenciadorArmazem

def typewriter(text, speed=0.05):
    for char in text:
        sleep(speed)
        sys.stdout.write(char)
        sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()

def exibir_introducao():
    titulo = "\n=== 🌻 BEM-VINDO(A) AO ARMAZÉM DO PIERRE (Stardew Valley) 🌻 ==="
    typewriter(titulo, speed=0.04)
 

def exibir_menu():
    print("================================================================")
    print("1. Inserir novo produto") 
    print("2. Alterar produto existente") 
    print("3. Pesquisar por nome") 
    print("4. Remover produto") 
    print("5. Listar todos os produtos") 
    print("6. Exibir um produto detalhado (com preço final!)") 
    print("7. Gerar Relatório do Fim do Dia") 
    print("0. Fechar a loja (Sair)")
    print("================================================================")

def main():
    db = GerenciadorArmazem()

    exibir_introducao()

    while True:
        # Menu principal
        print("\n=== MENU PRINCIPAL ===")
        print("1. Área do Cliente (Navegar / Comprar / Histórico)")
        print("2. Área do Funcionário (Armazém / Relatórios)")
        print("0. Sair")
        opcao_principal = input("Escolha: ")

        # Área do cliente
        if opcao_principal == '1':
            while True:
                print("\n🛒 --- ÁREA DO CLIENTE ---")
                print("1. Ver Catálogo (com Filtros Opcionais)")
                print("2. Fazer uma Compra")
                print("3. Ver Meu Histórico de Pedidos")
                print("0. Voltar")
                op_cli = input("Escolha: ")

                # Opção 1: Catálogo
                if op_cli == '1':
                    print("\n📦 --- CATÁLOGO ---")
                    print("1. Ver catálogo completo")
                    print("2. Filtrar catálogo")
                    op_cat = input("Escolha: ")

                    # Valor padrão eh sem filtro
                    nome = p_min = p_max = cat = mari = None

                    if op_cat == '2':
                        # Filtros opcionais
                        print("\n[Deixe em branco para não filtrar]")
                        nome  = input("Nome contém: ") or None
                        p_min_str = input("Preço mínimo (G): ")
                        p_max_str = input("Preço máximo (G): ")
                        cat   = input("Categoria (Semente/Cultivo/Coleta/Peixe): ") or None
                        mari_str  = input("Apenas fabricados em Mari-PB (S/N)? ").upper()

                        p_min = float(p_min_str) if p_min_str else None
                        p_max = float(p_max_str) if p_max_str else None
                        mari  = True if mari_str == 'S' else (False if mari_str == 'N' else None)
                    elif op_cat != '1':
                        print("Opção inválida.")
                        continue

                    produtos = db.listar_catalogo_filtrado(nome, p_min, p_max, cat, mari)
                    print("\n--- CATÁLOGO DO ARMAZÉM ---")
                    if produtos:
                        # Colunas: id, nome, preço, categoria, estoque, mari
                        for p in produtos:
                            tag_mari = " Mari-PB" if p[5] else ""
                            print(f"  [{p[0]}] {p[1]:<25} | {p[3]:<8} | {p[2]:>6.1f} G | Estoque: {p[4]} {tag_mari}")
                    else:
                        print("  Nenhum produto encontrado com esses filtros.")

                # Opção 2: Compra
                # Pede os dados do cliente (cadastro)
                elif op_cli == '2':
                    print("\n📝 --- CADASTRO PARA COMPRA ---")
                    print("Informe seus dados (usados para aplicar descontos especiais):")
                    nome_cli = input("Seu nome: ")
                    fla      = input("Torce pro Flamengo (S/N)? ").upper() == 'S'
                    op       = input("Assiste One Piece (S/N)?   ").upper() == 'S'
                    sousa    = input("É de Sousa-PB (S/N)?       ").upper() == 'S'

                    # Registra o cliente e calcula o desconto (10% por critério)
                    id_cli = db.registrar_cliente(nome_cli, fla, op, sousa)
                    desconto_possivel = (fla + op + sousa) * 10
                    print(f"\nBem-vindo(a), {nome_cli}! Desconto potencial: {desconto_possivel}%.")
                    if desconto_possivel > 0:
                        print("  (Aplicado ao finalizar a compra)")

                    # Indica o funcionário que vai realizar a venda
                    print("\nEscolha quem vai te atender:")
                    for v in db.listar_opcoes('vendedores'):
                        print(f"  [{v[0]}] {v[1]}")
                    id_vend = int(input("ID do Vendedor: "))

                    # Montagem do carrinho
                    print("\nAdicione produtos ao carrinho (ID 0 para finalizar):")
                    carrinho = []
                    while True:
                        id_prod = int(input("  ID do Produto (ou 0 para fechar carrinho): "))
                        if id_prod == 0:
                            break
                        qtd = int(input("  Quantidade: "))
                        carrinho.append({'id_prod': id_prod, 'qtd': qtd})

                    if not carrinho:
                        print("Carrinho vazio. Compra cancelada.")
                        continue

                    # Escolhe a forma de pagamento
                    print("\nComo deseja pagar?")
                    for fp in db.listar_opcoes('formas_pagamento'):
                        print(f"  [{fp[0]}] {fp[1]}")
                    id_pagamento = int(input("ID da Forma de Pagamento: "))

                    # Processa a venda todinha
                    sucesso, retorno = db.processar_venda_completa(id_cli, id_vend, id_pagamento, carrinho)

                    if sucesso:
                        print("\n  COMPRA REALIZADA COM SUCESSO!")
                        print(f"  Valor Bruto:          {retorno[0]:.1f} G")
                        print(f"  Desconto Aplicado:   -{retorno[1]:.1f} G")
                        print(f"  ─────────────────────────────")
                        print(f"  VALOR FINAL PAGO:     {retorno[2]:.1f} G")
                        print(f"\n  (Guarde seu ID de cliente [{id_cli}] para consultar o histórico!)")
                    else:
                        print(f"\n  ERRO NA COMPRA: {retorno}")

                # Opção 3: Histórico de Pedidos
                elif op_cli == '3':
                    print("\n📋 --- HISTÓRICO DE PEDIDOS ---")
                    try:
                        id_cli = int(input("Informe seu ID de cliente: "))
                        pedidos = db.historico_pedidos_cliente(id_cli)

                        if pedidos:
                            print(f"\nPedidos do cliente #{id_cli}:\n")
                            for p in pedidos:
                                # p = (id_venda, data_venda, forma_pag, status, bruto, desconto, liquido)
                                print(f"  Venda #{p[0]} | {p[1].strftime('%d/%m/%Y %H:%M')}")
                                print(f"    Pagamento: {p[2]} ({p[3]})")
                                print(f"    Bruto: {p[4]:.1f} G | Desconto: -{p[5]:.1f} G | Final: {p[6]:.1f} G")
                                print()
                        else:
                            print("  Nenhuma compra encontrada para este ID.")
                    except ValueError:
                        print("  ID inválido.")

                elif op_cli == '0':
                    break

        # Área do funcionário
        elif opcao_principal == '2':
            while True:
                print("\n --- ÁREA DO FUNCIONÁRIO ---")
                print("1. Gerenciar Produtos")
                print("2. Alerta de Estoque Baixo (< 5 unidades)")
                print("3. Relatório Mensal de Vendas por Vendedor")
                print("0. Voltar")
                op_func = input("Escolha: ")

                # Opção 1: Gerenciamento de produtos (CRUD)
                if op_func == '1':
                    while True:
                        print("\n --- GERENCIAR PRODUTOS ---")
                        print("1. Listar todos")
                        print("2. Exibir um produto")
                        print("3. Pesquisar por nome")
                        print("4. Inserir produto")
                        print("5. Alterar produto")
                        print("6. Remover produto")
                        print("7. Relatório geral do estoque")
                        print("0. Voltar")
                        op_crud = input("Escolha: ")

                        # Listar todos os produtos
                        if op_crud == '1':
                            produtos = db.listar_todos()
                            print("\n--- TODOS OS PRODUTOS ---")
                            for p in produtos:
                                # p = (id, nome, estoque, categoria, qualidade)
                                print(f"  [{p[0]}] {p[1]:<25} | {p[3]:<8} | {p[4]:<6} | Estoque: {p[2]}")

                        # Exibir detalhes de um produto pelo id
                        elif op_crud == '2':
                            try:
                                id_p = int(input("ID do produto: "))
                                p = db.exibir_um(id_p)
                                if p:
                                    print(f"\n  Nome:      {p['nome']}")
                                    print(f"  Categoria: {p['categoria']}")
                                    print(f"  Qualidade: {p['qualidade']}")
                                    print(f"  Estoque:   {p['estoque']} un.")
                                    print(f"  Preço:     {p['valor_unitario']:.1f} G")
                                else:
                                    print("  Produto não encontrado.")
                            except ValueError:
                                print("  ID inválido.")

                        # Pesquisar por nome
                        elif op_crud == '3':
                            nome_p = input("Nome contém: ")
                            resultados = db.pesquisar_por_nome(nome_p)
                            if resultados:
                                for p in resultados:
                                    print(f"  [{p[0]}] {p[1]} — Estoque: {p[2]}")
                            else:
                                print("  Nenhum produto encontrado.")

                        # Inserir novo produto
                        elif op_crud == '4':
                            try:
                                nome_p  = input("Nome do produto: ")
                                qtd     = int(input("Quantidade em estoque: "))

                                # Mostra categorias disponíveis para o funcionário escolher
                                print("Categorias disponíveis:")
                                for c in db.listar_opcoes('categorias'):
                                    print(f"  [{c[0]}] {c[1]} (base: {c[2]} G)")
                                id_cat  = int(input("ID da Categoria: "))

                                # Mostra qualidades disponíveis
                                print("Qualidades disponíveis:")
                                for q in db.listar_opcoes('qualidades'):
                                    print(f"  [{q[0]}] {q[1]} (x{q[2]})")
                                id_qual = int(input("ID da Qualidade: "))

                                mari_s  = input("Fabricado em Mari-PB (S/N)? ").upper() == 'S'

                                if db.inserir_produto(nome_p, qtd, id_cat, id_qual, mari_s):
                                    print("  Produto inserido com sucesso!")
                                else:
                                    print("  Falha ao inserir produto.")
                            except ValueError:
                                print("  Entrada inválida.")

                        # Alterar nome e/ou estoque de um produto
                        elif op_crud == '5':
                            try:
                                id_p     = int(input("ID do produto a alterar: "))
                                novo_nome = input("Novo nome (Enter para manter): ") or None
                                nova_qtd_s = input("Nova quantidade (Enter para manter): ")
                                nova_qtd  = int(nova_qtd_s) if nova_qtd_s else None

                                if db.alterar_produto(id_p, novo_nome, nova_qtd):
                                    print("  Produto atualizado!")
                                else:
                                    print("  Produto não encontrado ou nada alterado.")
                            except ValueError:
                                print("  Entrada inválida.")

                        # Remover produto pelo id
                        elif op_crud == '6':
                            try:
                                id_p = int(input("ID do produto a remover: "))
                                confirma = input(f"Tem certeza que quer remover o produto {id_p}? (S/N): ").upper()
                                if confirma == 'S':
                                    if db.remover_produto(id_p):
                                        print("  Produto removido.")
                                    else:
                                        print("  Produto não encontrado.")
                                else:
                                    print("  Remoção cancelada.")
                            except ValueError:
                                print("  ID inválido.")

                        # Relatório geral de estoque
                        elif op_crud == '7':
                            tipos, total, valor, categorias = db.gerar_relatorio()
                            
                            print(f"\n  Tipos de produto: {tipos}")
                            print(f"  Total de itens:   {total} unidades")
                            print(f"  Valor do estoque: {valor:.1f} G")
                            
                            print(f"\n  --- Quantidade por Categoria ---")
                            for cat, qtd in categorias.items():
                                print(f"    {cat}: {qtd} un.")

                        elif op_crud == '0':
                            break

                # Opção 2: Estoque baixo
                elif op_func == '2':
                    baixo_estoque = db.filtrar_estoque_baixo()
                    print("\n  ALERTA DE ESTOQUE BAIXO (< 5 unidades):")
                    if baixo_estoque:
                        for p in baixo_estoque:
                            print(f"  ID {p[0]} — {p[1]} (Restam {p[2]} un.)")
                    else:
                        print("  Tudo abastecido! Nenhum produto crítico.")

                # Opção 3: Relatório mensal
                elif op_func == '3':
                    try:
                        mes = int(input("\nMês (1-12): "))
                        ano = int(input("Ano (ex: 2026): "))
                        relatorio = db.relatorio_vendas_mensal(mes, ano)
                        print(f"\n RELATÓRIO DE VENDAS — {mes:02d}/{ano}:\n")
                        if relatorio:
                            for r in relatorio:
                                # r = (vendedor, total_vendas, total_arrecadado)
                                print(f"  {r[0]:<15} | {r[1]} venda(s) | {r[2]:.1f} G arrecadados")
                        else:
                            print("  Nenhuma venda confirmada neste período.")
                    except ValueError:
                        print("  Mês ou ano inválido.")

                elif op_func == '0':
                    break

        elif opcao_principal == '0':
            db.fechar_conexao()
            print("\nFechando a loja. Até amanhã! 🌻")
            break
        else:
            print("\nOpção inválida. Tente novamente.\n")
            sleep(0.5)

if __name__ == "__main__":
    main()

#a