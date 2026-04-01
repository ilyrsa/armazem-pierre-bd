import sys
import os
from time import sleep
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.text import Text
from rich import box

# Ajuste de caminho
sys.path.append(os.path.dirname(__file__))
from gerenciador import GerenciadorArmazem
from interface import InterfaceStardew

# Instâncias globais
console = Console()
interface = InterfaceStardew()

ARTE_DIREITA = """
╔══════════════════════════════════════╗
║                                      ║
║             ██████████               ║
║           ██████████████             ║
║          ████████████████            ║
║          ████░░░░░░░░█████           ║
║          ███░░░░░░░░░░░███           ║
║           ██░███░░░███░██            ║
║           ██░███░░░███░██            ║
║           ██░░░░░░░░░░░██            ║
║            █░░░░███░░░░█             ║
║             █░░░░░░░░░█              ║
║              █████████               ║
║                █████                 ║
║           ███████████████            ║
║        █████████████████████         ║
║      █████████████████████████       ║
║                                      ║
╚══════════════════════════════════════╝
"""

TITULO_ESQUERDA = """
   ╦ ╦ ╦ ╦═╗ ╦ ╦  ╔═╗
   ║ ║ ║ ╠╦╝ ╚╦╝  ╚═╗
   ╩ ╚═╝ ╩╚═  ╩   ╚═╝
 . iury s good store .
"""

def typewriter(text, speed=0.04):
    with console.capture() as capture:
        console.print(text, end="")
    str_renderizada = capture.get()
    
    for char in str_renderizada:
        sleep(speed)
        sys.stdout.write(char)
        sys.stdout.flush()
    print()

def gerar_layout() -> Layout:
    """Cria a estrutura da tela dividida (Menu Esquerda, Arte Direita)."""
    layout = Layout()
    layout.split_row(
        Layout(name="esquerda", ratio=2), # Menu e título ganham mais espaço
        Layout(name="direita", ratio=1)   # Arte ganha menos
    )
    layout["esquerda"].split_column(
        Layout(name="titulo", ratio=1),
        Layout(name="menu", ratio=3)
    )
    return layout

def atualizar_tela(layout: Layout, opcoes: list, indice_selecionado: int, titulo_menu: str):
    """Atualiza o conteúdo dos painéis com o tema Stardew Valley (Modo Iury)."""
    
    estilo_caixa = "on #f4b75e"
    
    cor_borda = "#561703"

    texto_arte = Text(ARTE_DIREITA, style="bold #680024")
    painel_arte = Panel(
        Align.center(texto_arte, vertical="middle"), 
        border_style=cor_borda, box=box.HEAVY, 
        title=f"[bold {cor_borda}]* Cliente VIP *[/]",
        style=estilo_caixa 
    )
    
    texto_titulo = Text(TITULO_ESQUERDA, style="bold #680024")
    painel_titulo = Panel(
        Align.center(texto_titulo, vertical="middle"),
        border_style=cor_borda, box=box.HEAVY, 
        title=f"[bold {cor_borda}]* ARMAZÉM DO IURY *[/]",
        style=estilo_caixa
    )
    
    texto_menu = Text()
    
    texto_menu.append(f"\n  {titulo_menu} \n\n", style="bold #561703") 
    
    for i, opcao in enumerate(opcoes):
        if i == indice_selecionado:
            texto_menu.append(f"  ► {opcao}\n", style="bold #571605")
        else:
            texto_menu.append(f"    {opcao}\n", style="bold #561703") 
            
    texto_menu.append("\n\nUse ↑ ↓ pra navegar e Enter pra selecionar", style="dim #561703")
    
    painel_menu = Panel(
        texto_menu, 
        border_style=cor_borda, box=box.HEAVY, 
        title=f"[bold {cor_borda}]* Menu *[/]",
        style=estilo_caixa
    )

    layout["direita"].update(painel_arte)
    layout["titulo"].update(painel_titulo)
    layout["menu"].update(painel_menu)

def menu_interativo(opcoes: list, titulo: str) -> int:
    """Roda o menu interativo e retorna o índice escolhido."""
    layout = gerar_layout()
    indice = 0
    with Live(layout, console=console, screen=True, refresh_per_second=15):
        while True:
            atualizar_tela(layout, opcoes, indice, titulo)
            tecla = readchar.readkey()
            if tecla == readchar.key.UP:
                indice = (indice - 1) % len(opcoes)
            elif tecla == readchar.key.DOWN:
                indice = (indice + 1) % len(opcoes)
            elif tecla == readchar.key.ENTER:
                return indice
            
def exibir_introducao():
    os.system('cls' if os.name == 'nt' else 'clear')
    titulo = Panel.fit(
        "[bold gold1]🌻 BEM-VINDO(A) AO ARMAZÉM DO IURY 🌻[/]\n[italic]Stardew Valley Edition[/]",
        border_style="#8B4513",
        padding=(1, 2)
    )
    console.print(titulo)
    typewriter("   [italic dark_orange]Preparando o estoque e limpando o balcão...[/]", 0.02)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        db = GerenciadorArmazem()
    except Exception:
        console.print("[bold red]❌ Erro ao conectar ao banco. O Docker está rodando?[/]")
        return

    # Loop Principal Interativo
    while True:
        opcoes_main = ["Área do Cliente", "Área do Funcionário", "Sair"]
        escolha_main = menu_interativo(opcoes_main, "MENU PRINCIPAL")

        if escolha_main == 2: # SAIR
            limpar_tela()
            db.fechar_conexao()
            console.print("\n[bold #8B4513]Fechando a loja. Até amanhã, Iury! 🌻[/]\n")
            break

        elif escolha_main == 0:
            while True:
                opcoes_cli = ["Ver Catálogo", "Fazer uma Compra", "Meu Histórico", "Voltar"]
                escolha_cli = menu_interativo(opcoes_cli, "ÁREA DO CLIENTE")

                if escolha_cli == 3: # Voltar
                    break

                limpar_tela()

                if escolha_cli == 0:
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

                elif escolha_cli == 1:
                    console.print(Panel("[bold]📝 IDENTIFICAÇÃO / CADASTRO[/]", border_style="cyan"))
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
                    
                    vendedores = db.listar_opcoes('vendedores')
                    tab_v = Table(show_header=False, border_style="blue")
                    for v in vendedores: tab_v.add_row(f"[{v[0]}]", v[1])
                    console.print("[bold]Escolha seu atendente:[/]")
                    console.print(tab_v)
                    id_vend = int(Prompt.ask("ID do Vendedor"))

                    console.print("\n[bold]🛒 ADICIONE AO CARRINHO (ID 0 para finalizar)[/]")
                    carrinho = []
                    while True:
                        id_p = int(Prompt.ask("ID do Produto"))
                        if id_p == 0: break
                        qtd = int(Prompt.ask("Quantidade"))
                        carrinho.append({'id_prod': id_p, 'qtd': qtd})

                    if carrinho:
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

                elif escolha_cli == 2:
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

                input("\n[Pressione ENTER para voltar ao menu...]")

        elif escolha_main == 1:
            while True:
                opcoes_func = [
                    "Gerenciar Produtos (CRUD)", 
                    "Alertas de Estoque Baixo", 
                    "Relatório Mensal de Vendas", 
                    "Ver Clientes Cadastrados", 
                    "Voltar"
                ]
                escolha_func = menu_interativo(opcoes_func, "ÁREA DO FUNCIONÁRIO")

                if escolha_func == 4: # Voltar
                    break

                limpar_tela()

                if escolha_func == 0:
                    while True:
                        opcoes_crud = [
                            "Listar todos", "Exibir um produto", "Pesquisar por nome", 
                            "Inserir produto", "Alterar produto", "Remover produto", 
                            "Relatório geral do estoque", "Voltar"
                        ]
                        escolha_crud = menu_interativo(opcoes_crud, "GERENCIAR PRODUTOS")
                        
                        if escolha_crud == 7: # Voltar
                            break
                        
                        limpar_tela()

                        if escolha_crud == 0:
                            produtos = db.listar_todos()
                            t_est = Table(title="📦 TODOS OS PRODUTOS")
                            t_est.add_column("ID"); t_est.add_column("Nome")
                            t_est.add_column("Categoria"); t_est.add_column("Qualidade"); t_est.add_column("Qtd", justify="right")
                            for p in produtos:
                                t_est.add_row(str(p[0]), p[1], p[3], p[4], str(p[2]))
                            console.print(t_est)

                        elif escolha_crud == 1:
                            try:
                                id_p = int(Prompt.ask("ID do produto"))
                                p = db.exibir_um(id_p)
                                if p:
                                    detalhes = f"Nome: {p['nome']}\nCategoria: {p['categoria']}\nQualidade: {p['qualidade']}\nEstoque: {p['estoque']} un.\nPreço Unitário: [green]{p['valor_unitario']:.1f} G[/]"
                                    console.print(Panel(detalhes, title=f"Detalhes do ID {id_p}", border_style="cyan"))
                                else:
                                    console.print("[red]Produto não encontrado.[/]")
                            except ValueError:
                                console.print("[red]ID inválido.[/]")

                        elif escolha_crud == 2:
                            nome_p = Prompt.ask("Nome contém")
                            resultados = db.pesquisar_por_nome(nome_p)
                            if resultados:
                                for p in resultados: console.print(f"  [{p[0]}] {p[1]} — Estoque: {p[2]}")
                            else:
                                console.print("[yellow]Nenhum produto encontrado.[/]")

                        elif escolha_crud == 3:
                            try:
                                n = Prompt.ask("Nome do produto")
                                q = int(Prompt.ask("Quantidade em estoque"))
                                
                                console.print("\n[bold]Categorias disponíveis:[/]")
                                for c in db.listar_opcoes('categorias'): console.print(f"  [{c[0]}] {c[1]} (base: {c[2]} G)")
                                c_id = int(Prompt.ask("ID Categoria"))
                                
                                console.print("\n[bold]Qualidades disponíveis:[/]")
                                for ql in db.listar_opcoes('qualidades'): console.print(f"  [{ql[0]}] {ql[1]} (x{ql[2]})")
                                q_id = int(Prompt.ask("ID Qualidade"))
                                
                                m = Prompt.ask("Fabricado em Mari-PB? (S/N)", choices=["S", "N"]) == 'S'
                                
                                if db.inserir_produto(n, q, c_id, q_id, m):
                                    console.print("[green]✔ Produto inserido com sucesso![/]")
                                else:
                                    console.print("[red]❌ Falha ao inserir produto.[/]")
                            except ValueError:
                                console.print("[red]Entrada inválida.[/]")

                        elif escolha_crud == 4:
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

                        elif escolha_crud == 5:
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

                        elif escolha_crud == 6:
                            tipos, total, valor, categorias = db.gerar_relatorio()
                            rel = f"Tipos de produto: {tipos}\nTotal de itens: {total} unidades\nValor do estoque: [green]{valor:.1f} G[/]\n\n[bold]--- Quantidade por Categoria ---[/]\n"
                            for c, q in categorias.items(): rel += f"  {c}: {q} un.\n"
                            console.print(Panel(rel, title="📊 Relatório Geral do Estoque", border_style="cyan"))

                        input("\n[Pressione ENTER para voltar...]")

                elif escolha_func == 1:
                    baixo = db.filtrar_estoque_baixo()
                    console.print("\n[bold red]  ALERTA DE ESTOQUE BAIXO (< 5 unidades):[/]")
                    if baixo:
                        for b in baixo: console.print(f"  ID {b[0]} — {b[1]} (Restam [red]{b[2]}[/] un.)")
                    else:
                        console.print("  [green]Tudo abastecido! Nenhum produto crítico.[/]")
                    input("\n[Pressione ENTER para voltar ao menu...]")

                elif escolha_func == 2:
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
                    input("\n[Pressione ENTER para voltar ao menu...]")

                elif escolha_func == 3:
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
                    input("\n[Pressione ENTER para voltar ao menu...]")

if __name__ == "__main__":
    main()