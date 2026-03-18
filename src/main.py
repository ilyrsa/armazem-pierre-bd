import sys
import os
from time import sleep

# Adiciona o diretório atual ao sys.path para permitir importações locais
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
    titulo = "\n=== 🌻 BEM-VINDO(A) AO ARMAZÉM DO PIERRE 🌻 ==="
    typewriter(titulo, speed=0.04)
    sleep(1)

def exibir_menu():
    print("================================================================")
    print("1. Inserir novo produto") 
    print("2. Alterar produto existente") 
    print("3. Pesquisar por nome") 
    print("4. Remover produto") 
    print("5. Listar todos os produtos") 
    print("6. Exibir um produto detalhado com preço final") 
    print("7. Gerar Relatório do Fim do Dia") 
    print("0. Fechar a loja (Sair)")
    print("================================================================")

def main():
    gerenciador = GerenciadorArmazem()

    exibir_introducao()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("\nNome do item (ex: Vinho de Carambola): ")
            qtd = int(input("\nQuantidade em estoque: "))
            
            print("\nCategorias: 1-Semente, 2-Cultivo, 3-Coleta, 4-Peixe, 5-Produto Artesanal")
            id_cat = int(input("\nID da Categoria: "))
            
            print("\nQualidades: 1-Normal, 2-Prata, 3-Ouro, 4-Irídio")
            id_qual = int(input("\nID da Qualidade: "))

            print() # Pula linha antes da mensagem de sucesso
            if gerenciador.inserir_produto(nome, qtd, id_cat, id_qual):
                print("Item guardado no baú com sucesso!\n")
            else:
                print("Ops, erro ao inserir item.\n")

            sleep(0.5)

        elif opcao == '2':
            id_prod = int(input("\nID do produto que deseja alterar: "))
            novo_nome = input("\nNovo nome: ")
            nova_qtd = int(input("\nNova quantidade: "))
            
            print()
            if gerenciador.alterar_produto(id_prod, novo_nome, nova_qtd):
                print("Item alterado com sucesso!\n")
            else:
                print("Item não encontrado.\n")

            sleep(0.5)

        elif opcao == '3':
            nome_pesquisa = input("\nDigite o nome para pesquisar: ")
            print()
            resultados = gerenciador.pesquisar_por_nome(nome_pesquisa)
            if resultados:
                for p in resultados:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Estoque: {p[2]} | Cat: {p[3]} | Qual: {p[4]}")
                print()
            else:
                print("Nenhum item encontrado com esse nome.\n")

            sleep(0.5)

        elif opcao == '4':
            id_prod = int(input("\nID do produto a ser removido: "))
            print()
            if gerenciador.remover_produto(id_prod):
                print("O item foi jogado no lixo com sucesso!\n")
            else:
                print("Item não encontrado.\n")

            sleep(0.5)

        elif opcao == '5':
            produtos = gerenciador.listar_todos()
            if produtos:
                print("\n--- Inventário Completo ---\n")
                for p in produtos:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Estoque: {p[2]} un. | Tipo: {p[3]} | Qualidade: {p[4]}")
                print()
            else:
                print("\nO baú está vazio!\n")

            sleep(0.5)

        elif opcao == '6':
            id_prod = int(input("\nID do produto para exibir detalhes: "))
            produto = gerenciador.exibir_um(id_prod)
            if produto:
                print("\n--- Detalhes do Item ---")
                print(f"\nNome: {produto['nome']}")
                print(f"\nEstoque: {produto['estoque']}")
                print(f"\nCategoria: {produto['categoria']}")
                print(f"\nQualidade: {produto['qualidade']}")
                print(f"\nValor final de venda: {produto['valor_unitario']}g\n")
            else:
                print("\nItem não encontrado.\n")

            sleep(0.5)

        elif opcao == '7':
            total_itens, valor_caixa = gerenciador.gerar_relatorio()
            print("\n === RELATÓRIO DE FIM DE DIA === ")
            print(f"\nTotal de itens guardados: {total_itens}")
            print(f"\nValor total do estoque: {valor_caixa}g\n")

            sleep(0.5)

        elif opcao == '0':
            typewriter("\nFechando o Armazém.")
            sleep(0.2)
            typewriter("Até logo! ~ Pierre 🌻")
            gerenciador.fechar_conexao()
            break
        else:
            print("\nOpção inválida. Tente novamente.\n")
            sleep(0.5)

if __name__ == "__main__":
    main()