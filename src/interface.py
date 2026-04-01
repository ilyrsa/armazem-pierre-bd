from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box

class InterfaceStardew:
    def __init__(self):
        self.console = Console()
        self.COR_MADEIRA = "#8B4513"
        self.COR_MENU = "#FFD700"
        self.COR_ESTOQUE = "#32CD32"
        self.COR_FUNDO_HEX = "#f4b75e"
        self.ESTILO_FUNDO = "on #f4b75e"
        self.COR_VINHO = "#561703"
        self.COR_FONTE = "bold #680024"
        self.COR_BORDA = "#000000"

    def exibir_catalogo(self, produtos):

        tabela = Table(
            title=f"[{self.COR_FONTE}] ARMAZÉM DO IURY — CATÁLOGO [/]",
            border_style=self.COR_BORDA,
            header_style=f"bold {self.COR_VINHO}",
            show_lines=True,
            box=box.HEAVY,
            style=self.ESTILO_FUNDO
        )

        # Tudo em bold black, exceto preço em bold green
        tabela.add_column("ID",        style="bold black", justify="center")
        tabela.add_column("Item",      style="bold black")
        tabela.add_column("Categoria", style="bold black")
        tabela.add_column("Preço",     justify="right", style="bold green")
        tabela.add_column("Estoque",   justify="center")
        tabela.add_column("Origem",    justify="center")

        for p in produtos:
            id_p, nome, preco, cat, estoque, mari = p

            cor_estoque = "bold red" if estoque < 5 else "bold black"
            # Mari-PB em bold pink, Importado em bold black
            tag_mari = "[bold pink]✦ Mari-PB[/]" if mari else "[bold black]Importado[/]"

            tabela.add_row(
                str(id_p),
                f"[bold black]{nome}[/]",
                f"[bold black]{cat}[/]",
                f"[bold green]{preco:.1f} G[/]",
                f"[{cor_estoque}]{estoque}[/]",
                tag_mari
            )

        self.console.print("\n")
        self.console.print(Align.center(tabela))
        self.console.print("\n")

    def exibir_recibo_pixel(self, bruto, desconto, liquido):

        conteudo = Text()
        # Adicionado bold em todos os textos para legibilidade
        conteudo.append(f"  Subtotal:           {bruto:.1f} G\n",    style=f"bold {self.COR_VINHO}")
        conteudo.append(f"  Desconto aplicado: -{desconto:.1f} G\n", style=f"bold {self.COR_VINHO}")
        conteudo.append("  ══════════════════════════\n",            style=f"bold {self.COR_BORDA}")
        conteudo.append(f"  TOTAL RECEBIDO:     {liquido:.1f} G",    style=f"bold {self.COR_VINHO}")

        recibo = Panel(
            Align.center(conteudo, vertical="middle"),
            title=f"[bold {self.COR_VINHO}]* Recibo de Venda *[/]",
            border_style=self.COR_BORDA,
            subtitle=f"[bold italic {self.COR_VINHO}]Obrigado por comprar conosco! 🌻[/]",
            box=box.HEAVY,
            style=self.ESTILO_FUNDO,
            width=46
        )
        self.console.print("\n")
        self.console.print(Align.center(recibo))
        self.console.print("\n")