import pandas as pd
from faker import Faker
import random

# Inicializar Faker
faker = Faker("pt_BR")

# Dados base para geração
aulas = {
    "Aula de guitarra": {
        "professor": "Carlos",
        "alunos": ["Rafaela", "Debora", "Marcos", "Pedro", "Vinícius"],
    },
    "Aula de violão": {
        "professor": "Pedro",
        "alunos": ["Ana Paula", "Renato", "Sandro"],
    },
    "Aula de baixo": {"professor": "Mayara", "alunos": ["Renata", "Livia", "Felipe"]},
    "Aula de piano": {"professor": "Camila", "alunos": ["João", "Henrique"]},
    "Aula de canto": {
        "professor": "Roberto",
        "alunos": ["Hugo", "Gabriel", "Sara", "Teresa", "Beatriz"],
    },
    "Teatro": {"professor": "Luana", "alunos": ["Kaline", "Joana", "Jessica"]},
    "Aula de musicalização Infantil": {
        "professor": "Lais",
        "alunos": ["Vitor", "Allan", "Milena"],
    },
}

fornecedores = ["Prestação de serviço", "Despesas Fixas", "Despesas Variáveis"]
despesas_fixas_variaveis = ["Produtos de limpeza", "Comida", "Material de escritório"]


# Função para gerar uma data aleatória entre 2024 e 2025
def gerar_data_aleatoria():
    return faker.date_between_dates(
        date_start=pd.Timestamp("2024-01-01"), date_end=pd.Timestamp("2025-12-31")
    )


# Função para gerar uma transação de aula
def gerar_transacao_aula(nome_aula):
    dados = aulas[nome_aula]
    professor = dados["professor"]
    aluno = random.choice(dados["alunos"])
    participantes = f"{professor}, {aluno}"
    receita = 52.50
    despesa = 25.00
    return {
        "Nome da Transação": nome_aula,
        "Data do Evento": gerar_data_aleatoria(),
        "Participantes": participantes,
        "Receita": receita,
        "Despesa": despesa,
    }


# Função para gerar uma transação de fornecedor/despesa
def gerar_transacao_fornecedor(nome_fornecedor):
    if nome_fornecedor == "Prestação de serviço":
        participante = faker.company()
        despesa = round(random.uniform(150.0, 300.0), 2)  # Prestação de serviço
    else:
        participante = random.choice(despesas_fixas_variaveis)
        despesa = round(random.uniform(50.0, 180.0), 2)  # Despesas fixas/variáveis
    receita = 0.0  # Nenhuma receita gerada para fornecedores
    return {
        "Nome da Transação": nome_fornecedor,
        "Data do Evento": gerar_data_aleatoria(),
        "Participantes": participante,
        "Receita": receita,
        "Despesa": despesa,
    }


# Gerar 440 registros de aulas
registros_aulas = [
    gerar_transacao_aula(random.choice(list(aulas.keys()))) for _ in range(440)
]

# Gerar 220 registros de fornecedores/despesas
registros_fornecedores = [
    gerar_transacao_fornecedor(random.choice(fornecedores)) for _ in range(220)
]

# Combinar os registros
registros_combinados = registros_aulas + registros_fornecedores

# Criar DataFrame
df_novo = pd.DataFrame(registros_combinados)

# Salvar em Excel
df_novo.to_excel("novo_arquivo_financeiro.xlsx", index=False)
