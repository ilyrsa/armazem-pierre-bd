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
    sleep(1)

def exibir_introducao():
    titulo = "\n=== 🌻 BEM-VINDO(A) AO ARMAZÉM DO PIERRE (Stardew Valley) 🌻 ===\n"
    typewriter(titulo, speed=0.04)
    sleep(1)

def exibir_menu():
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
    # Classe gerenciadora instanciada
    gerenciador = GerenciadorArmazem()

    exibir_introducao()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do item (ex: Vinho de Carambola): ")
            qtd = int(input("Quantidade em estoque: "))
            
            print("\nCategorias: 1-Semente, 2-Cultivo, 3-Coleta, 4-Peixe, 5-Produto Artesanal")
            id_cat = int(input("ID da Categoria: "))
            
            print("Qualidades: 1-Normal, 2-Prata, 3-Ouro, 4-Irídio")
            id_qual = int(input("ID da Qualidade: "))

            if gerenciador.inserir_produto(nome, qtd, id_cat, id_qual):
                print("✅ Item guardado no baú com sucesso!")
            else:
                print("❌ Erro ao inserir item.")

            sleep(0.5)

        elif opcao == '2':
            id_prod = int(input("ID do produto que deseja alterar: "))
            novo_nome = input("Novo nome: ")
            nova_qtd = int(input("Nova quantidade: "))
            if gerenciador.alterar_produto(id_prod, novo_nome, nova_qtd):
                print("✅ Produto alterado com sucesso!")
            else:
                print("❌ Produto não encontrado.")

            sleep(0.5)

        elif opcao == '3':
            nome_pesquisa = input("Digite o nome para pesquisar: ")
            resultados = gerenciador.pesquisar_por_nome(nome_pesquisa)
            if resultados:
                for p in resultados:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Estoque: {p[2]} | Cat: {p[3]} | Qual: {p[4]}")
            else:
                print("Nenhum item encontrado com esse nome.")

            sleep(0.5)

        elif opcao == '4':
            id_prod = int(input("ID do produto a ser removido: "))
            if gerenciador.remover_produto(id_prod):
                print("🗑️ Produto jogado no lixo com sucesso!")
            else:
                print("❌ Produto não encontrado.")

            sleep(0.5)

        elif opcao == '5':
            produtos = gerenciador.listar_todos()
            if produtos:
                print("\n--- Inventário Completo ---")
                for p in produtos:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Estoque: {p[2]} un. | Tipo: {p[3]} | Qualidade: {p[4]}")
            else:
                print("O baú está vazio!")

            sleep(0.5)

        elif opcao == '6':
            id_prod = int(input("ID do produto para exibir detalhes: "))
            produto = gerenciador.exibir_um(id_prod)
            if produto:
                print("\n--- Detalhes do Item ---")
                print(f"Nome: {produto['nome']}")
                print(f"Estoque: {produto['estoque']}")
                print(f"Categoria: {produto['categoria']}")
                print(f"Qualidade: {produto['qualidade']}")
                print(f"💰 VALOR FINAL DE VENDA: {produto['valor_unitario']}g")
                print()
            else:
                print("❌ Produto não encontrado.")
                print()

            sleep(0.5)

        elif opcao == '7':
            total_itens, valor_caixa = gerenciador.gerar_relatorio()
            print("\n📦 === RELATÓRIO DE FIM DE DIA === 📦")
            print(f"Total de itens guardados: {total_itens}")
            print(f"Valor total do estoque: {valor_caixa}g")
            print("===================================")
            print()

            sleep(0.5)

        elif opcao == '0':
            typewriter("\nFechando o Armazém.")
            sleep(0.2)
            typewriter("Até logo! ~ Pierre 🌻")
            gerenciador.fechar_conexao()
            break
        else:
            print("Opção inválida. Tente novamente.")

            sleep(0.5)

if __name__ == "__main__":
    main()