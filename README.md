# Armazém do Pierre (Stardew Valley) - Sistema de Estoque

## Descrição do projeto

Este projeto é a **Parte 1** da avaliação da disciplina de Banco de Dados I. Consiste em um sistema CRUD (Create, Read, Update, Delete) em console para gerenciar o estoque de uma "Bodega/Agricultura" inspirada no universo de Stardew Valley 

**Tecnologias utilizadas:** Python 3 e PostgreSQL.

## Estrutura

```bash
ArmazemStardewValley/
├── src/                  # Código-fonte principal
│   ├── main.py           # Interface
│   └── gerenciador.py    # Classe GerenciadorArmazem (Isola a lógica SQL e o CRUD)
├── db/                   # Arquivos relacionados ao banco de dados
│   ├── setup_banco.py    # Script DDL/DML para criar tabelas e popular categorias base
│   └── banco.db          # Arquivo do banco PostreSQL (Gerado localmente, ignorado no Git)
├── docs/                 # Documentação exigida pelo projeto
│   └── diagrama_UML.pdf  # Diagrama de Classes UML
├── .gitignore            # Arquivos ignorados pelo controle de versão (*.db, venv/, etc.)
├── requirements.txt      # Dependências do projeto (Bibliotecas externas, se houver)
└── README.md             # Apresentação do projeto e instruções de uso

```

## Como rodar
Siga os passos abaixo para inicializar o banco de dados e rodar a aplicação na sua máquina (comandos baseados em terminais Linux/macOS):

### 1. Clone o repositório e entre na pasta principal:

```bash 
git clone <COLOQUE_AQUI_O_LINK_DO_SEU_REPOSITORIO>
cd ArmazemStardewValley
```

### 2. (Opcional, mas recomendado) Crie e ative o ambiente virtual:

```bash 
python3 -m venv venv
source venv/bin/activate
```

### 3. Construa o Banco de Dados (rodar só uma vez):
O arquivo de banco de dados (banco.db) não é versionado no Git. Você precisa rodar o script de setup para criar as tabelas e inserir as categorias/qualidades originais do jogo na sua máquina local.

```bash 
python3 db/setup_banco.py
```

### 4. Abra a loja e gerencie o estoque:
Sempre que quiser iniciar o sistema, basta executar a interface principal.

``` bash
python3 src/main.py
```

