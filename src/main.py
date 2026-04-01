import sys
import os
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

# Ajuste de caminho
sys.path.append(os.path.dirname(__file__))
from gerenciador import GerenciadorArmazem
from interface import InterfaceStardew

# Instâncias globais
console = Console()
interface = InterfaceStardew()

def typewriter(text, speed=0.04):
    with console.capture() as capture:
        console.print(text, end="")
    str_renderizada = capture.get()
    
    for char in str_renderizada:
        sleep(speed)
        sys.stdout.write(char)
        sys.stdout.flush()
    print()

def exibir_introducao():
    os.system('cls' if os.name == 'nt' else 'clear')
    titulo = Panel.fit(
        "[bold gold1]🌻 BEM-VINDO(A) AO ARMAZÉM DO PIERRE 🌻[/]\n[italic]Stardew Valley Edition[/]",
        border_style="#8B4513",
        padding=(1, 2)
    )
    console.print(titulo)
    typewriter("   [italic dark_orange]Preparando o estoque e limpando o balcão...[/]", 0.02)

def main():
    try:
        db = GerenciadorArmazem()
    except Exception:
        console.print("[bold red] Erro ao conectar ao banco. O Docker está rodando?[/]")
        return

    exibir_introducao()

    while True:
        console.print(Panel("[bold]MENU PRINCIPAL[/]\n\n1.  [cyan]Área do Cliente[/]\n2.  [orange1]Área do Funcionário[/]\n0.  [red]Sair[/]", border_style="#8B4513"))
        
        opcao_principal = Prompt.ask("Escolha uma opção", choices=["1", "2", "0"])

        # É do cliente aqui ó
        if opcao_principal == '1':
            while True:
                console.print("\n[bold cyan]─── ÁREA DO CLIENTE ───[/]")
                print("1. Ver Catálogo\n2. Fazer uma Compra\n3. Meu Histórico\n0. Voltar")
                op_cli = Prompt.ask("Escolha", choices=["1", "2", "3", "0"])

                if op_cli == '1':
                    op_cat = Prompt.ask("\n[1] Catálogo Completo\n[2] Filtrar Catálogo", choices=["1", "2"])
                    
                    nome = p_min = p_max = cat = mari = None
                    
                    if op_cat == '2': 
                        console.print("[italic]Deixe em branco para não filtrar um campo.[/]")
                        nome = Prompt.ask("Nome contém") or None
                        
                        p_min_str = Prompt.ask("Preço mínimo (G)")
                        p_min = float(p_min_str) if p_min_str else None
                        
                        p_max_str = Prompt.ask("Preço máximo (G)")
                        p_max = float(p_max_str) if p_max_str else None
                        
                        cat = Prompt.ask("Categoria (Semente/Cultivo/etc)") or None
                        
                        mari_str = Prompt.ask("Apenas fabricados em Mari-PB? (S/N)", choices=["S", "N", ""])
                        mari = True if mari_str == 'S' else (False if mari_str == 'N' else None)

                    produtos = db.listar_catalogo_filtrado(nome, p_min, p_max, cat, mari)
                    if produtos:
                        interface.exibir_catalogo(produtos)
                    else:
                        console.print("\n[yellow]  Nenhum produto encontrado com esses filtros.[/]")

                elif op_cli == '2':
                    console.print(Panel("[bold] IDENTIFICAÇÃO / CADASTRO[/]", border_style="cyan"))
                    console.print("[italic]Informe seus dados para aplicar descontos especiais:[/]")
                    nome_cli = Prompt.ask("Seu nome")
                    fla = Prompt.ask("Torce pro Flamengo? (S/N)", choices=["S", "N"]) == "S"
                    op = Prompt.ask("Assiste One Piece? (S/N)", choices=["S", "N"]) == "S"
                    sousa = Prompt.ask("É de Sousa-PB? (S/N)", choices=["S", "N"]) == "S"

                    id_cli = db.registrar_cliente(nome_cli, fla, op, sousa)
                    desconto_possivel = (fla + op + sousa) * 10
                    console.print(f"\n[bold green]✔ Cliente {nome_cli} identificado! (ID: {id_cli})[/]")
                    if desconto_possivel > 0:
                        console.print(f"[bold yellow]Você possui até {desconto_possivel}% de desconto nesta compra![/]\n")
                    
                    # Seleção de Vendedor
                    vendedores = db.listar_opcoes('vendedores')
                    tab_v = Table(show_header=False, border_style="blue")
                    for v in vendedores: tab_v.add_row(f"[{v[0]}]", v[1])
                    console.print("[bold]Escolha seu atendente:[/]")
                    console.print(tab_v)
                    id_vend = int(Prompt.ask("ID do Vendedor"))

                    # Carrinho
                    console.print("\n[bold]🛒 ADICIONE AO CARRINHO (ID 0 para finalizar)[/]")
                    carrinho = []
                    while True:
                        id_p = int(Prompt.ask("ID do Produto"))
                        if id_p == 0: break
                        qtd = int(Prompt.ask("Quantidade"))
                        carrinho.append({'id_prod': id_p, 'qtd': qtd})

                    if carrinho:
                        # Pagamento
                        pagamentos = db.listar_opcoes('formas_pagamento')
                        for fp in pagamentos: console.print(f"[{fp[0]}] {fp[1]}")
                        id_pag = int(Prompt.ask("Forma de Pagamento"))

                        sucesso, retorno = db.processar_venda_completa(id_cli, id_vend, id_pag, carrinho)
                        if sucesso:
                            interface.exibir_recibo_pixel(retorno[0], retorno[1], retorno[2])
                            console.print(f"  [dim](Guarde seu ID de cliente [{id_cli}] para histórico!)[/]\n")
                        else:
                            console.print(f"\n[bold red]❌ ERRO NA COMPRA: {retorno}[/]\n")
                    else:
                        console.print("[yellow]Carrinho vazio. Compra cancelada.[/]")

                elif op_cli == '3':
                    id_c = Prompt.ask("Informe seu ID de cliente")
                    try:
                        pedidos = db.historico_pedidos_cliente(int(id_c))
                        if pedidos:
                            t_hist = Table(title=f"🌻 HISTÓRICO DE COMPRAS - CLIENTE #{id_c} 🌻", border_style="magenta")
                            t_hist.add_column("ID Venda"); t_hist.add_column("Data", justify="center")
                            t_hist.add_column("Pagamento", justify="center"); t_hist.add_column("Total Pago", style="bold green", justify="right")

                            for p in pedidos:
                                data_formatada = p[1].strftime('%d/%m/%Y %H:%M')
                                t_hist.add_row(str(p[0]), data_formatada, str(p[2]), f"{p[6]:.1f} G")
                            console.print(t_hist)
                        else:
                            console.print("[yellow]⚠ Nenhuma compra encontrada para este ID.[/]")
                    except ValueError:
                        console.print("[red]❌ ID inválido.[/]")
                    except Exception as e:
                        console.print(f"[red]❌ Erro ao buscar histórico: {e}[/]")

                elif op_cli == '0': break

        # Área do funcionário aqui ó
        elif opcao_principal == '2':
            while True:
                console.print("\n[bold orange1]─── ÁREA DO FUNCIONÁRIO ───[/]")
                print("1. Gerenciar Produtos (CRUD)")
                print("2. Alertas de Estoque Baixo (< 5 unidades)")
                print("3. Relatório Mensal de Vendas por Vendedor")
                print("4. Ver Clientes Cadastrados")
                print("0. Voltar")
                op_func = Prompt.ask("Escolha", choices=["1", "2", "3", "4", "0"])

                if op_func == '1':
                    while True:
                        console.print("\n[bold yellow]--- GERENCIAR PRODUTOS ---[/]")
                        print("1. Listar todos")
                        print("2. Exibir um produto")
                        print("3. Pesquisar por nome")
                        print("4. Inserir produto")
                        print("5. Alterar produto")
                        print("6. Remover produto")
                        print("7. Relatório geral do estoque")
                        print("0. Voltar")
                        op_crud = Prompt.ask("Escolha", choices=["1","2","3","4","5","6","7","0"])

                        if op_crud == '1':
                            produtos = db.listar_todos()
                            t_est = Table(title="📦 TODOS OS PRODUTOS")
                            t_est.add_column("ID"); t_est.add_column("Nome")
                            t_est.add_column("Categoria"); t_est.add_column("Qualidade"); t_est.add_column("Qtd", justify="right")
                            for p in produtos:
                                # p = (id, nome, estoque, categoria, qualidade)
                                t_est.add_row(str(p[0]), p[1], p[3], p[4], str(p[2]))
                            console.print(t_est)

                        elif op_crud == '2':
                            id_p = Prompt.ask("ID do produto")
                            try:
                                p = db.exibir_um(int(id_p))
                                if p:
                                    detalhes = f"Nome: {p['nome']}\nCategoria: {p['categoria']}\nQualidade: {p['qualidade']}\nEstoque: {p['estoque']} un.\nPreço Unitário: [green]{p['valor_unitario']:.1f} G[/]"
                                    console.print(Panel(detalhes, title=f"Detalhes do ID {id_p}", border_style="cyan"))
                                else:
                                    console.print("[red]Produto não encontrado.[/]")
                            except ValueError:
                                console.print("[red]ID inválido.[/]")

                        elif op_crud == '3':
                            nome_p = Prompt.ask("Nome contém")
                            resultados = db.pesquisar_por_nome(nome_p)
                            if resultados:
                                for p in resultados: console.print(f"  [{p[0]}] {p[1]} — Estoque: {p[2]}")
                            else:
                                console.print("[yellow]Nenhum produto encontrado.[/]")

                        elif op_crud == '4':
                            try:
                                n = Prompt.ask("Nome do produto")
                                q = int(Prompt.ask("Quantidade em estoque"))
                                
                                console.print("\n[bold]Categorias disponíveis:[/]")
                                for c in db.listar_opcoes('categorias'): print(f"  [{c[0]}] {c[1]} (base: {c[2]} G)")
                                c_id = int(Prompt.ask("ID Categoria"))
                                
                                console.print("\n[bold]Qualidades disponíveis:[/]")
                                for ql in db.listar_opcoes('qualidades'): print(f"  [{ql[0]}] {ql[1]} (x{ql[2]})")
                                q_id = int(Prompt.ask("ID Qualidade"))
                                
                                m = Prompt.ask("Fabricado em Mari-PB? (S/N)", choices=["S", "N"]) == 'S'
                                
                                if db.inserir_produto(n, q, c_id, q_id, m):
                                    console.print("[green]✔ Produto inserido com sucesso![/]")
                                else:
                                    console.print("[red]❌ Falha ao inserir produto.[/]")
                            except ValueError:
                                console.print("[red]Entrada inválida.[/]")

                        elif op_crud == '5':
                            try:
                                id_p = int(Prompt.ask("ID do produto a alterar"))
                                n = Prompt.ask("Novo nome (Enter para manter)") or None
                                q_str = Prompt.ask("Nova quantidade (Enter para manter)")
                                q = int(q_str) if q_str else None
                                
                                if db.alterar_produto(id_p, n, q):
                                    console.print("[green]✔ Produto atualizado![/]")
                                else:
                                    console.print("[red]Produto não encontrado ou nada alterado.[/]")
                            except ValueError:
                                console.print("[red]Entrada inválida.[/]")

                        elif op_crud == '6':
                            try:
                                id_p = int(Prompt.ask("ID do produto a remover"))
                                confirma = Prompt.ask(f"Tem certeza que quer remover o ID {id_p}? (S/N)", choices=["S", "N"])
                                if confirma == 'S':
                                    if db.remover_produto(id_p):
                                        console.print("[green]✔ Produto removido do sistema.[/]")
                                    else:
                                        console.print("[red]Produto não encontrado.[/]")
                                else:
                                    console.print("[yellow]Remoção cancelada.[/]")
                            except ValueError:
                                console.print("[red]ID inválido.[/]")

                        elif op_crud == '7':
                            tipos, total, valor, categorias = db.gerar_relatorio()
                            rel = f"Tipos de produto: {tipos}\nTotal de itens: {total} unidades\nValor do estoque: [green]{valor:.1f} G[/]\n\n[bold]--- Quantidade por Categoria ---[/]\n"
                            for c, q in categorias.items(): rel += f"  {c}: {q} un.\n"
                            console.print(Panel(rel, title=" Relatório Geral do Estoque", border_style="cyan"))

                        elif op_crud == '0': break

                elif op_func == '2':
                    baixo = db.filtrar_estoque_baixo()
                    console.print("\n[bold red]  ALERTA DE ESTOQUE BAIXO (< 5 unidades):[/]")
                    if baixo:
                        for b in baixo: console.print(f"  ID {b[0]} — {b[1]} (Restam [red]{b[2]}[/] un.)")
                    else:
                        console.print("  [green]Tudo abastecido! Nenhum produto crítico.[/]")

                elif op_func == '3': 
                    try:
                        mes = int(Prompt.ask("Mês (1-12)"))
                        ano = int(Prompt.ask("Ano (ex: 2026)"))
                        relatorio = db.relatorio_vendas_mensal(mes, ano)
                        if relatorio:
                            t_rel = Table(title=f"RELATÓRIO DE VENDAS — {mes:02d}/{ano}", border_style="cyan")
                            t_rel.add_column("Vendedor"); t_rel.add_column("Vendas"); t_rel.add_column("Total Arrecadado", style="green")
                            for r in relatorio: 
                                t_rel.add_row(r[0], f"{r[1]} venda(s)", f"{r[2]:.1f} G")
                            console.print(t_rel)
                        else:
                            console.print("\n[yellow]  Nenhuma venda confirmada neste período.[/]")
                    except ValueError:
                        console.print("[red]Mês ou ano inválido.[/]")

                elif op_func == '4':
                    clientes = db.listar_clientes()
                    t_cli = Table(title="👥 CLIENTES CADASTRADOS")
                    t_cli.add_column("ID")
                    t_cli.add_column("Nome")
                    t_cli.add_column("Tags/Descontos")
                    for c in clientes:
                        tags = []
                        if c[2]: tags.append("Flamenguista")
                        if c[3]: tags.append("One Piece")
                        if c[4]: tags.append("De Sousa-PB")
                        tags_str = ", ".join(tags) if tags else "Nenhuma"
                        t_cli.add_row(str(c[0]), c[1], f"[dim]{tags_str}[/]")
                    console.print(t_cli)

                elif op_func == '0': break

        elif opcao_principal == '0':
            db.fechar_conexao()
            console.print("\n[bold #8B4513]Até amanhã, Pierre! 🌻[/]")
            break

if __name__ == "__main__":
    main()