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

sys.path.append(os.path.dirname(__file__))
from gerenciador import GerenciadorArmazem
from interface import InterfaceStardew

console = Console()
interface = InterfaceStardew()

ESTILO_FUNDO = "on #f4b75e"
COR_BORDA    = "#000000"
COR_FONTE    = "bold #680024"

# ─────────────────────────────── ARTE ──────────────────────────────────────

ARTE_DIREITA = r"""
                                                    
                                                    
                                                    
                     @@@@@@@@@@                         
                @@%%#%%#%#####%%@                       
               @%%#%#*####***##*##@                     
              @%##%#**##%@@%%#**##@@                    
              @%#####*#%##**#@%##%%%@                   
             @%%*+--=====--+%#@%%%%#%@                  
             @=:............-@%=%#%#%@                  
             #::............:@-:%#%#%@                  
             #+=-=-....:-----++#-#%%#%                  
             #@#**%-...:#***#@*::%+..:#                 
             #%-.=:#%%##..===#..:-.-+:#                 
             +.%..#-...-#...#-..::.=+-#                 
             =....-.............:=::+#                  
             #:...++--:.........:*%#                    
              #:................+#                      
               #:.-##+##+......:+#                      
                #-..-=--:....-+=-#                      
                  :.......:-#---.=#                     
                   #=---=#+-:.....#                     
                      #--=:.......:#                    
                 %%@@**...........:*#@#                 
           *##@%#*@@@@#.........%%@@@@@###@#@           
       %##@@@@@%%@@@@@%@@#---@%@@@%%%%@@%%@@@@@##       
      ####*###**###**###****#****####*****########      
     %#######*#####*****#*########******##########%     
     %%#%#%%###%%%@@@%%%%%%%%%%%%%%::%.%%%%#####%%%* 
     *%%##%%%%%@@@%%::%@%%%%%%%%%%@.%-:=%@@@@%#%###%%%

                    ╦ ╦ ╦ ╦═╗ ╦ ╦  ╔═╗
                    ║ ║ ║ ╠╦╝ ╚╦╝  ╚═╗
                    ╩ ╚═╝ ╩╚═  ╩   ╚═╝
                
"""

TITULO_ESQUERDA = r"""
   ╔╗ ╔═╗╔╦╗ ╦  ╦╦╔╗╔╔╦╗╔═╗  ╔═╗╔═╗  ╔═╗╦═╗╔╦╗╔═╗╔═╗╔═╗╔╦╗  ╔╦╗╔═╗  ╦╦ ╦╦═╗╦ ╦
   ╠╩╗║╣ ║║║ ╚╗╔╝║║║║ ║║║ ║  ╠═╣║ ║  ╠═╣╠╦╝║║║╠═╣╔ ╝║╣ ║║║   ║║║ ║  ║║ ║╠╦╝╚╦╝
   ╚═╝╚═╝╩ ╩  ╚╝ ╩╝╚╝ ╩ ╚═╝  ╩ ╩╚═╝  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝╚═╝╩ ╩  ╩ ╩╚═╝  ╩╚═╝╩╚═ ╩ 
                      
"""

TITULO_LOGO = r"""
   ╔═╗╦═╗╔╦╗╔═╗╔═╗╔═╗╔╦╗  ╔╦╗╔═╗  ╦╦ ╦╦═╗╦ ╦
   ╠═╣╠╦╝║║║╠═╣╔ ╝║╣ ║║║   ║║║ ║  ║║ ║╠╦╝╚╦╝
   ╩ ╩╩╚═╩ ╩╩ ╩╚═╝╚═╝╩ ╩  ╩ ╩╚═╝  ╩╚═╝╩╚═ ╩ 
                      
"""

# ─────────────────────────────── HELPERS ───────────────────────────────────

def configurar_fundo_terminal():
    sys.stdout.write("\033]11;#f4b75e\007")
    sys.stdout.write("\033[48;2;244;183;94m\033[2J\033[H")
    sys.stdout.flush()

def painel(titulo: str, conteudo, subtitulo: str = "") -> Panel:
    return Panel(
        conteudo,
        title=f"[{COR_FONTE}]* {titulo} *[/]",
        subtitle=f"[dim {COR_BORDA}]{subtitulo}[/]" if subtitulo else "",
        border_style=COR_BORDA,
        box=box.HEAVY,
        style=ESTILO_FUNDO
    )

def tabela_stardew(titulo: str, *colunas) -> Table:
    t = Table(
        title=f"[{COR_FONTE}]{titulo}[/]",
        border_style=COR_BORDA,
        header_style=f"bold {COR_BORDA}",
        show_lines=True,
        box=box.HEAVY,
        style=ESTILO_FUNDO
    )
    for col in colunas:
        if isinstance(col, dict):
            t.add_column(**col)
        else:
            t.add_column(col, style=f"bold {COR_BORDA}")
    return t

def prompt_stardew(pergunta: str, **kwargs) -> str:
    return Prompt.ask(f"[bold {COR_BORDA}]{pergunta}[/]", **kwargs)

def aviso(msg: str, tipo: str = "info"):
    estilos = {
        "info":   f"bold {COR_FONTE}",
        "ok":     f"bold {COR_FONTE}",
        "erro":   "bold red",
        "alerta": f"bold {COR_BORDA}",
    }
    console.print(f"\n  [{estilos.get(tipo, COR_FONTE)}]{msg}[/]\n")

# ─────────────────────────────── MENU ──────────────────────────────────────

def gerar_layout() -> Layout:
    layout = Layout()
    layout.split_row(
        Layout(name="esquerda", ratio=2),
        Layout(name="direita",  ratio=1)
    )
    layout["esquerda"].split_column(
        Layout(name="titulo", ratio=1),
        Layout(name="menu",   ratio=3)
    )
    return layout

def atualizar_tela(layout: Layout, opcoes: list, indice_selecionado: int, titulo_menu: str):
    estilo_caixa = ESTILO_FUNDO

    texto_arte = Text(ARTE_DIREITA, style=COR_FONTE)
    painel_arte = Panel(
        Align.center(texto_arte, vertical="middle"),
        border_style=COR_BORDA, box=box.HEAVY,
        title=f"[{COR_FONTE}]* Você é nosso Cliente VIP! *[/]",
        style=estilo_caixa
    )

    texto_titulo = Text(TITULO_ESQUERDA, style=COR_FONTE)
    painel_titulo = Panel(
        Align.center(texto_titulo, vertical="middle"),
        border_style=COR_BORDA, box=box.HEAVY,
        title=f"[{COR_FONTE}]* ARMAZÉM DO IURY *[/]",
        style=estilo_caixa
    )

    texto_menu = Text()
    texto_menu.append(f"\n  {titulo_menu} \n\n", style=f"bold {COR_BORDA}")
    for i, opcao in enumerate(opcoes):
        if i == indice_selecionado:
            texto_menu.append(f"  ► {opcao}\n", style=f"bold {COR_BORDA}")
        else:
            texto_menu.append(f"    {opcao}\n", style=f"bold {COR_BORDA}")
    texto_menu.append("\n\nUse ↑ ↓ pra navegar e Enter pra selecionar", style=f"dim {COR_BORDA}")

    painel_menu = Panel(
        texto_menu,
        border_style=COR_BORDA, box=box.HEAVY,
        title=f"[{COR_FONTE}]* Menu *[/]",
        style=estilo_caixa
    )

    layout["direita"].update(painel_arte)
    layout["titulo"].update(painel_titulo)
    layout["menu"].update(painel_menu)

def menu_interativo(opcoes: list, titulo: str) -> int:
    layout = gerar_layout()
    painel_geral = Panel(
        layout,
        border_style=COR_BORDA,
        box=box.HEAVY,
        style=ESTILO_FUNDO,
        padding=(1, 2),
        expand=True
    )
    
    indice = 0
    with Live(painel_geral, console=console, screen=True, refresh_per_second=15):
        while True:
            atualizar_tela(layout, opcoes, indice, titulo)
            tecla = readchar.readkey()
            if tecla == readchar.key.UP:
                indice = (indice - 1) % len(opcoes)
            elif tecla == readchar.key.DOWN:
                indice = (indice + 1) % len(opcoes)
            elif tecla == readchar.key.ENTER:
                return indice

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def cabecalho_tela(subtitulo: str = ""):
    limpar_tela()
    texto = Text(TITULO_LOGO, style=COR_FONTE)
    sub = f"[dim {COR_BORDA}]  {subtitulo}[/]" if subtitulo else ""
    console.print(Panel(
        Align.center(texto, vertical="middle"),
        border_style=COR_BORDA,
        box=box.HEAVY,
        style=ESTILO_FUNDO,
        subtitle=sub
    ))
    console.print()

# ─────────────────────────────── MAIN ──────────────────────────────────────

def main():
    configurar_fundo_terminal()
    try:
        db = GerenciadorArmazem()
    except Exception:
        console.print("[bold red] Erro ao conectar ao banco. O Docker está rodando?[/]")
        return

    while True:
        opcoes_main = ["Área do Cliente", "Área do Funcionário", "Sair"]
        escolha_main = menu_interativo(opcoes_main, "MENU PRINCIPAL")

        # ── SAIR ─────────────────────────────────────────────────────────────
        if escolha_main == 2:
            limpar_tela()
            db.fechar_conexao()
            console.print(painel(
                "Até logo!",
                Align.center(Text("\nFechando a loja. Até amanhã ~ Iury!\n", style=COR_FONTE))
            ))
            break

        # ── ÁREA DO CLIENTE ───────────────────────────────────────────────────
        elif escolha_main == 0:
            while True:
                opcoes_cli = ["Ver Catálogo", "Fazer uma Compra", "Meu Histórico", "Voltar"]
                escolha_cli = menu_interativo(opcoes_cli, "ÁREA DO CLIENTE")

                if escolha_cli == 3:
                    break

                # ── VER CATÁLOGO ──────────────────────────────────────────────
                if escolha_cli == 0:
                    cabecalho_tela("Ver Catálogo")
                    op_cat = prompt_stardew(
                        "\n[1] Catálogo Completo\n[2] Filtrar Catálogo",
                        choices=["1", "2"]
                    )
                    nome = p_min = p_max = cat = mari = None

                    if op_cat == '2':
                        console.print(painel(
                            "Filtrar Catálogo",
                            Text("  Deixe em branco para não filtrar um campo.\n", style=f"dim {COR_BORDA}")
                        ))
                        nome      = prompt_stardew("Nome contém") or None
                        p_min_str = prompt_stardew("Preço mínimo (G)")
                        p_min     = float(p_min_str) if p_min_str else None
                        p_max_str = prompt_stardew("Preço máximo (G)")
                        p_max     = float(p_max_str) if p_max_str else None
                        cat       = prompt_stardew("Categoria (Semente/Cultivo/etc)") or None
                        mari_str  = prompt_stardew("Apenas fabricados em Mari-PB? (S/N)", choices=["S", "N", ""])
                        mari      = True if mari_str == 'S' else (False if mari_str == 'N' else None)

                    produtos = db.listar_catalogo_filtrado(nome, p_min, p_max, cat, mari)
                    if produtos:
                        interface.exibir_catalogo(produtos)
                    else:
                        aviso("Nenhum produto encontrado com esses filtros.", "alerta")

                # ── FAZER UMA COMPRA ──────────────────────────────────────────
                elif escolha_cli == 1:
                    cabecalho_tela("Fazer uma Compra")
                    console.print(painel(
                        "Identificação / Cadastro",
                        Text("  Informe seus dados para aplicar descontos especiais:\n", style=f"bold {COR_BORDA}")
                    ))

                    nome_cli = prompt_stardew("Seu nome")
                    fla   = prompt_stardew("Torce pro Flamengo? (S/N)", choices=["S", "N"]) == "S"
                    op    = prompt_stardew("Assiste One Piece? (S/N)",  choices=["S", "N"]) == "S"
                    sousa = prompt_stardew("É de Sousa-PB? (S/N)",      choices=["S", "N"]) == "S"

                    id_cli = db.registrar_cliente(nome_cli, fla, op, sousa)
                    desconto_possivel = (fla + op + sousa) * 10

                    cabecalho_tela("Fazer uma Compra")
                    t_id = Text()
                    t_id.append(f"  Cliente {nome_cli} identificado! (ID: {id_cli})\n", style=f"bold {COR_FONTE}")
                    if desconto_possivel > 0:
                        t_id.append(f"  Você possui até {desconto_possivel}% de desconto nesta compra! 🎉\n", style=f"bold {COR_FONTE}")
                    console.print(painel("Bem-vindo!", t_id))

                    vendedores = db.listar_opcoes('vendedores')
                    t_v = tabela_stardew(
                        "Escolha seu Atendente",
                        {"header": "ID",   "justify": "center"},
                        {"header": "Nome", "style": f"bold {COR_BORDA}"}
                    )
                    for v in vendedores:
                        t_v.add_row(str(v[0]), v[1])
                    console.print(Align.center(t_v))
                    id_vend = int(prompt_stardew("ID do Vendedor"))

                    cabecalho_tela("Fazer uma Compra")
                    console.print(painel(
                        "Carrinho de Compras",
                        Text("  Adicione produtos ao carrinho.\n  Digite 0 para finalizar.\n", style=f"bold {COR_BORDA}")
                    ))
                    carrinho = []
                    while True:
                        id_p = int(prompt_stardew("ID do Produto"))
                        if id_p == 0:
                            break
                        qtd = int(prompt_stardew("Quantidade"))
                        carrinho.append({'id_prod': id_p, 'qtd': qtd})

                    if carrinho:
                        cabecalho_tela("Fazer uma Compra")
                        pagamentos = db.listar_opcoes('formas_pagamento')
                        t_pag = tabela_stardew(
                            "Forma de Pagamento",
                            {"header": "ID",   "justify": "center"},
                            {"header": "Forma", "style": f"bold {COR_BORDA}"}
                        )
                        for fp in pagamentos:
                            t_pag.add_row(str(fp[0]), fp[1])
                        console.print(Align.center(t_pag))
                        id_pag = int(prompt_stardew("Forma de Pagamento"))

                        sucesso, retorno = db.processar_venda_completa(id_cli, id_vend, id_pag, carrinho)
                        if sucesso:
                            interface.exibir_recibo_pixel(retorno[0], retorno[1], retorno[2])
                            console.print(f"  [dim {COR_BORDA}](Guarde seu ID de cliente [{id_cli}] para histórico!)[/]\n")
                        else:
                            aviso(f"ERRO NA COMPRA: {retorno}", "erro")
                    else:
                        aviso("Carrinho vazio. Compra cancelada.", "alerta")

                # ── MEU HISTÓRICO ─────────────────────────────────────────────
                elif escolha_cli == 2:
                    cabecalho_tela("Meu Histórico")
                    id_c = prompt_stardew("Informe seu ID de cliente")
                    try:
                        pedidos = db.historico_pedidos_cliente(int(id_c))
                        if pedidos:
                            t_hist = tabela_stardew(
                                f"🌻 Histórico de Compras — Cliente #{id_c} 🌻",
                                {"header": "ID Venda",   "justify": "center"},
                                {"header": "Data",       "justify": "center"},
                                {"header": "Pagamento",  "justify": "center"},
                                {"header": "Total Pago", "justify": "right", "style": f"bold {COR_BORDA}"}
                            )
                            for p in pedidos:
                                data_formatada = p[1].strftime('%d/%m/%Y %H:%M')
                                t_hist.add_row(str(p[0]), data_formatada, str(p[2]), f"{p[6]:.1f} G")
                            console.print(Align.center(t_hist))
                        else:
                            aviso("Nenhuma compra encontrada para este ID.", "alerta")
                    except ValueError:
                        aviso("ID inválido.", "erro")
                    except Exception as e:
                        aviso(f"Erro ao buscar histórico: {e}", "erro")

                input(f"\n Pressione ENTER para voltar ao menu...[/]")

        # ── ÁREA DO FUNCIONÁRIO ───────────────────────────────────────────────
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

                if escolha_func == 4:
                    break

                # ── CRUD PRODUTOS ─────────────────────────────────────────────
                if escolha_func == 0:
                    while True:
                        opcoes_crud = [
                            "Listar todos", "Exibir um produto", "Pesquisar por nome",
                            "Inserir produto", "Alterar produto", "Remover produto",
                            "Relatório geral do estoque", "Voltar"
                        ]
                        escolha_crud = menu_interativo(opcoes_crud, "GERENCIAR PRODUTOS")

                        if escolha_crud == 7:
                            break

                        cabecalho_tela("Gerenciar Produtos")

                        if escolha_crud == 0:
                            produtos = db.listar_todos()
                            t_est = tabela_stardew(
                                "Todos os Produtos",
                                {"header": "ID",        "justify": "center"},
                                {"header": "Nome"},
                                {"header": "Categoria"},
                                {"header": "Qualidade"},
                                {"header": "Qtd",       "justify": "right"}
                            )
                            for p in produtos:
                                t_est.add_row(str(p[0]), p[1], p[3], p[4], str(p[2]))
                            console.print(Align.center(t_est))

                        elif escolha_crud == 1:
                            try:
                                id_p = int(prompt_stardew("ID do produto"))
                                p = db.exibir_um(id_p)
                                if p:
                                    det = Text()
                                    det.append(f"  Nome:          {p['nome']}\n",               style=f"bold {COR_FONTE}")
                                    det.append(f"  Categoria:     {p['categoria']}\n",           style=f"bold {COR_FONTE}")
                                    det.append(f"  Qualidade:     {p['qualidade']}\n",           style=f"bold {COR_FONTE}")
                                    det.append(f"  Estoque:       {p['estoque']} un.\n",         style=f"bold {COR_FONTE}")
                                    det.append(f"  Preço Unit.:   {p['valor_unitario']:.1f} G",  style=f"bold {COR_FONTE}")
                                    console.print(painel(f"Detalhes — ID {id_p}", det))
                                else:
                                    aviso("Produto não encontrado.", "erro")
                            except ValueError:
                                aviso("ID inválido.", "erro")

                        elif escolha_crud == 2:
                            nome_p = prompt_stardew("Nome contém")
                            resultados = db.pesquisar_por_nome(nome_p)
                            if resultados:
                                t_res = tabela_stardew(
                                    f"Resultados para '{nome_p}'",
                                    {"header": "ID",      "justify": "center"},
                                    {"header": "Nome"},
                                    {"header": "Estoque", "justify": "right"}
                                )
                                for p in resultados:
                                    t_res.add_row(str(p[0]), p[1], str(p[2]))
                                console.print(Align.center(t_res))
                            else:
                                aviso("Nenhum produto encontrado.", "alerta")

                        elif escolha_crud == 3:
                            try:
                                n = prompt_stardew("Nome do produto")
                                q = int(prompt_stardew("Quantidade em estoque"))

                                cats = db.listar_opcoes('categorias')
                                t_c = tabela_stardew(
                                    "Categorias Disponíveis",
                                    {"header": "ID",       "justify": "center"},
                                    {"header": "Nome"},
                                    {"header": "Base (G)", "justify": "right"}
                                )
                                for c in cats:
                                    t_c.add_row(str(c[0]), c[1], f"{c[2]} G")
                                console.print(Align.center(t_c))
                                c_id = int(prompt_stardew("ID Categoria"))

                                qls = db.listar_opcoes('qualidades')
                                t_q = tabela_stardew(
                                    "Qualidades Disponíveis",
                                    {"header": "ID",          "justify": "center"},
                                    {"header": "Nível"},
                                    {"header": "Multiplicador", "justify": "right"}
                                )
                                for ql in qls:
                                    t_q.add_row(str(ql[0]), ql[1], f"x{ql[2]}")
                                console.print(Align.center(t_q))
                                q_id = int(prompt_stardew("ID Qualidade"))

                                m = prompt_stardew("Fabricado em Mari-PB? (S/N)", choices=["S", "N"]) == 'S'

                                if db.inserir_produto(n, q, c_id, q_id, m):
                                    aviso("✔ Produto inserido com sucesso!", "ok")
                                else:
                                    aviso("Falha ao inserir produto.", "erro")
                            except ValueError:
                                aviso("Entrada inválida.", "erro")

                        elif escolha_crud == 4:
                            try:
                                id_p = int(prompt_stardew("ID do produto a alterar"))
                                n    = prompt_stardew("Novo nome (Enter para manter)") or None
                                q_str = prompt_stardew("Nova quantidade (Enter para manter)")
                                q    = int(q_str) if q_str else None

                                if db.alterar_produto(id_p, n, q):
                                    aviso("✔ Produto atualizado!", "ok")
                                else:
                                    aviso("Produto não encontrado ou nada alterado.", "alerta")
                            except ValueError:
                                aviso("Entrada inválida.", "erro")

                        elif escolha_crud == 5:
                            try:
                                id_p = int(prompt_stardew("ID do produto a remover"))
                                confirma = prompt_stardew(f"Tem certeza que quer remover o ID {id_p}? (S/N)", choices=["S", "N"])
                                if confirma == 'S':
                                    if db.remover_produto(id_p):
                                        aviso("✔ Produto removido do sistema.", "ok")
                                    else:
                                        aviso("Produto não encontrado.", "erro")
                                else:
                                    aviso("Remoção cancelada.", "alerta")
                            except ValueError:
                                aviso("ID inválido.", "erro")

                        elif escolha_crud == 6:
                            tipos, total, valor, categorias = db.gerar_relatorio()
                            rel = Text()
                            rel.append(f"  Tipos de produto:  {tipos}\n",                    style=f"bold {COR_FONTE}")
                            rel.append(f"  Total de itens:    {total} unidades\n",           style=f"bold {COR_FONTE}")
                            rel.append(f"  Valor do estoque:  {valor:.1f} G\n\n",            style=f"bold {COR_FONTE}")
                            rel.append("  ── Quantidade por Categoria ──\n",                 style=f"bold {COR_BORDA}")
                            for c, q in categorias.items():
                                rel.append(f"    {c}: {q} un.\n",                            style=f"bold {COR_FONTE}")
                            console.print(painel("Relatório Geral do Estoque", rel))

                        input(f"\n Pressione ENTER para voltar...[/]")

                # ── ALERTAS DE ESTOQUE BAIXO ──────────────────────────────────
                elif escolha_func == 1:
                    cabecalho_tela("Alertas de Estoque Baixo")
                    baixo = db.filtrar_estoque_baixo()
                    if baixo:
                        t_al = tabela_stardew(
                            "⚠ Alerta — Estoque Baixo (< 5 unidades)",
                            {"header": "ID",      "justify": "center"},
                            {"header": "Produto"},
                            {"header": "Qtd",     "justify": "right", "style": "bold red"}
                        )
                        for b in baixo:
                            t_al.add_row(str(b[0]), b[1], str(b[2]))
                        console.print(Align.center(t_al))
                    else:
                        aviso("Tudo abastecido! Nenhum produto crítico. ✔", "ok")
                    input(f"\n Pressione ENTER para voltar ao menu...[/]")

                # ── RELATÓRIO MENSAL ──────────────────────────────────────────
                elif escolha_func == 2:
                    cabecalho_tela("Relatório Mensal de Vendas")
                    try:
                        mes = int(prompt_stardew("Mês (1-12)"))
                        ano = int(prompt_stardew("Ano (ex: 2026)"))
                        relatorio = db.relatorio_vendas_mensal(mes, ano)
                        if relatorio:
                            t_rel = tabela_stardew(
                                f"Relatório de Vendas — {mes:02d}/{ano}",
                                {"header": "Vendedor"},
                                {"header": "Vendas",           "justify": "center"},
                                {"header": "Total Arrecadado", "justify": "right"}
                            )
                            for r in relatorio:
                                t_rel.add_row(r[0], f"{r[1]} venda(s)", f"{r[2]:.1f} G")
                            console.print(Align.center(t_rel))
                        else:
                            aviso("Nenhuma venda confirmada neste período.", "alerta")
                    except ValueError:
                        aviso("Mês ou ano inválido.", "erro")
                    input(f"\n Pressione ENTER para voltar ao menu...[/]")

                # ── VER CLIENTES ──────────────────────────────────────────────
                elif escolha_func == 3:
                    cabecalho_tela("Clientes Cadastrados")
                    clientes = db.listar_clientes()
                    t_cli = tabela_stardew(
                        "👥 Clientes Cadastrados",
                        {"header": "ID",           "justify": "center"},
                        {"header": "Nome"},
                        {"header": "Tags/Descontos"}
                    )
                    for c in clientes:
                        tags = []
                        if c[2]: tags.append("Flamenguista")
                        if c[3]: tags.append("One Piece")
                        if c[4]: tags.append("De Sousa-PB")
                        tags_str = ", ".join(tags) if tags else "Nenhuma"
                        t_cli.add_row(str(c[0]), c[1], f"[dim {COR_BORDA}]{tags_str}[/]")
                    console.print(Align.center(t_cli))
                    input(f"\n Pressione ENTER para voltar ao menu...[/]")

if __name__ == "__main__":
    main()
