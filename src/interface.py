from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align

class InterfaceStardew:
    def __init__(self):
        self.console = Console()
        # Cores temáticas do Stardew
        self.COR_MADEIRA = "#8B4513" # SaddleBrown
        self.COR_MENU = "#FFD700"    # Gold
        self.COR_ESTOQUE = "#32CD32" # LimeGreen

    def exibir_catalogo(self, produtos):
        # Tabela estilizada como o menu do Pierre
        tabela = Table(
            title="[bold #FFD700]🌿 ARMAZÉM DO PIERRE - CATÁLOGO 🌿[/]",
            border_style=self.COR_MADEIRA,
            header_style="bold #DEB887",
            show_lines=True
        )
        
        tabela.add_column("ID", style="gold1", justify="center")
        tabela.add_column("Item", style="white")
        tabela.add_column("Categoria", style="italic cyan")
        tabela.add_column("Preço", justify="right", style="bold green")
        tabela.add_column("Estoque", justify="center")
        tabela.add_column("Origem", justify="center")

        for p in produtos:
            # p = (id, nome, preço, categoria, estoque, mari)
            id_p, nome, preco, cat, estoque, mari = p
            
            # Lógica de cores para estoque baixo
            cor_estoque = "red" if estoque < 5 else "white"
            tag_mari = "[bold #E91E63]Mari-PB[/]" if mari else "[grey50]Importado[/]"
            
            tabela.add_row(
                str(id_p), 
                f"[bold]{nome}[/]", 
                cat, 
                f"{preco:.1f} G", 
                f"[{cor_estoque}]{estoque}[/]",
                tag_mari
            )

        self.console.print("\n")
        self.console.print(Align.center(tabela))
        self.console.print("\n")

    def exibir_recibo_pixel(self, bruto, desconto, liquido):
        # Um painel que imita a cartinha do Prefeito Lewis
        conteudo = Text()
        conteudo.append(f"Subtotal: {bruto:.1f} G\n", style="white")
        conteudo.append(f"Bônus/Desconto: -{desconto:.1f} G\n", style="bold green")
        conteudo.append("──────────────────────────\n", style=self.COR_MADEIRA)
        conteudo.append(f"TOTAL RECEBIDO: {liquido:.1f} G", style="bold gold1")

        recibo = Panel(
            Align.center(conteudo),
            title="[bold white]✉️ Recibo de Venda[/]",
            border_style=self.COR_MADEIRA,
            subtitle="[italic]Obrigado por comprar local![/]",
            width=40
        )
        self.console.print(Align.center(recibo))

    def cabecalho_estacao(self, estacao="Primavera"):
        # Um banner decorativo para o topo
        banner = Panel(
            Align.center(f"[bold #FFD700]✨ {estacao.upper()} - ANO 1 ✨[/]\n[italic]Clima: Ensolarado ☀️[/]"),
            border_style="#228B22", # ForestGreen
            padding=(1, 2)
        )
        self.console.print(banner)