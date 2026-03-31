import sys
import os
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Ajuste de caminho para importar seus arquivos
sys.path.append(os.path.dirname(__file__))
from gerenciador import GerenciadorArmazem
from interface import InterfaceStardew

# Instâncias globais
console = Console()
interface = InterfaceStardew()

def typewriter(text, speed=0.04):
    # O segredo: renderizar o texto com as cores do Rich antes de imprimir
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
        console.print("[bold red]❌ Erro ao conectar ao banco. O Docker está rodando?[/]")
        return

    exibir_introducao()

    while True:
        console.print(Panel("[bold]MENU PRINCIPAL[/]\n\n1. 🧺 [cyan]Área do Cliente[/]\n2. 💼 [orange1]Área do Funcionário[/]\n0. 🚪 [red]Sair[/]", border_style="#8B4513"))
        
        opcao_principal = Prompt.ask("Escolha uma opção", choices=["1", "2", "0"])

        if opcao_principal == '1':
            while True:
                console.print("\n[bold cyan]─── ÁREA DO CLIENTE ───[/]")
                print("1. Ver Catálogo\n2. Fazer uma Compra\n3. Meu Histórico\n0. Voltar")
                op_cli = Prompt.ask("Escolha", choices=["1", "2", "3", "0"])

                if op_cli == '1':
                    nome = Prompt.ask("Filtrar por nome? (Deixe vazio para todos)") or None
                    produtos = db.listar_catalogo_filtrado(nome=nome)
                    interface.exibir_catalogo(produtos) # Usando sua classe Interface!

                # No trecho da Opção 2 (Fazer uma Compra), mude para:
                elif op_cli == '2':
                    console.print(Panel("[bold]📝 IDENTIFICAÇÃO / CADASTRO[/]", border_style="cyan"))
                    nome_cli = Prompt.ask("Seu nome")
                    
                    # O banco agora usa UPSERT (se já existe, não duplica)
                    fla = Prompt.ask("Torce pro Flamengo?", choices=["S", "N"]) == "S"
                    op = Prompt.ask("Assiste One Piece?", choices=["S", "N"]) == "S"
                    sousa = Prompt.ask("É de Sousa-PB?", choices=["S", "N"]) == "S"

                    id_cli = db.registrar_cliente(nome_cli, fla, op, sousa)
                    
                    # ROTINA DE ID: Informa ao usuário qual o ID dele
                    console.print(f"\n[bold green]✔ Cliente identificado! Seu ID é: {id_cli}[/]\n")
                    
                    # Segue para a seleção de vendedor...
                    
                    # Seleção de Vendedor com Tabela
                    vendedores = db.listar_opcoes('vendedores')
                    tab_v = Table(show_header=False, border_style="blue")
                    for v in vendedores: tab_v.add_row(f"[{v[0]}]", v[1])
                    console.print("\n[bold]Escolha seu atendente:[/]")
                    console.print(tab_v)
                    id_vend = int(Prompt.ask("ID do Vendedor"))

                    # Carrinho
                    carrinho = []
                    while True:
                        id_p = int(Prompt.ask("ID do Produto (0 para finalizar)"))
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
                            recibo = Panel(
                                f"Bruto: {retorno[0]:.1f} G\nDesconto: -{retorno[1]:.1f} G\n[bold green]TOTAL: {retorno[2]:.1f} G[/]",
                                title="✅ VENDA REALIZADA", border_style="green"
                            )
                            console.print(recibo)
                        else:
                            console.print(f"[bold red]❌ ERRO: {retorno}[/]")

                elif op_cli == '3':
                    id_c = Prompt.ask("Informe seu ID de cliente")
                    try:
                        pedidos = db.historico_pedidos_cliente(int(id_c))
                        if pedidos:
                            t_hist = Table(title=f"🌻 HISTÓRICO DE COMPRAS - CLIENTE #{id_c} 🌻", border_style="magenta")
                            t_hist.add_column("Data", justify="center")
                            t_hist.add_column("Itens Comprados", style="italic") # Nova coluna!
                            t_hist.add_column("Pagamento", justify="center")
                            t_hist.add_column("Total (G)", style="bold green", justify="right")

                            for p in pedidos:
                                # p[1]: data_venda, p[3]: itens (texto agrupado), p[4]: forma_pagamento, p[6]: valor_liquido
                                data_formatada = p[1].strftime('%d/%m/%Y %H:%M')
                                itens = p[3] if p[3] else "Itens não registrados"
                                pagamento = str(p[4])
                                total = f"{p[6]:.1f} G"
                                
                                t_hist.add_row(data_formatada, itens, pagamento, total)
                            
                            console.print(t_hist)
                        else:
                            console.print("[yellow]⚠ Nenhum pedido encontrado para este ID.[/]")
                    except ValueError:
                        console.print("[red]❌ ID inválido. Por favor, digite um número.[/]")
                    except Exception as e:
                        console.print(f"[red]❌ Erro ao buscar histórico: {e}[/]")

                elif op_cli == '0': 
                    break

        elif opcao_principal == '2':
            while True:
                console.print("\n[bold orange1]─── ÁREA DO FUNCIONÁRIO ───[/]")
                print("1. Gerenciar Estoque\n2. Alertas\n3. Clientes\n0. Voltar")
                op_func = Prompt.ask("Escolha", choices=["1", "2", "3", "0"])

                if op_func == '1':
                    produtos = db.listar_todos()
                    t_est = Table(title="📦 ESTOQUE ATUAL")
                    t_est.add_column("ID")
                    t_est.add_column("Nome")
                    t_est.add_column("Qtd", justify="right")
                    for p in produtos:
                        cor = "red" if p[2] < 5 else "white"
                        t_est.add_row(str(p[0]), p[1], f"[{cor}]{p[2]}[/]")
                    console.print(t_est)

                elif op_func == '2':
                    baixo = db.filtrar_estoque_baixo()
                    if baixo:
                        for b in baixo: console.print(f"[bold red]⚠ BAIXO ESTOQUE:[/] {b[1]} ({b[2]} un.)")
                    else:
                        console.print("[green]✅ Estoque em dia![/]")

                elif op_func == '3':
                    clientes = db.listar_clientes()
                    t_cli = Table(title="👥 CLIENTES CADASTRADOS")
                    t_cli.add_column("ID")
                    t_cli.add_column("Nome")
                    for c in clientes: t_cli.add_row(str(c[0]), c[1])
                    console.print(t_cli)

                elif op_func == '0': break

        elif opcao_principal == '0':
            db.fechar_conexao()
            console.print("\n[bold #8B4513]Até amanhã, Pierre! 🌻[/]")
            break

if __name__ == "__main__":
    main()