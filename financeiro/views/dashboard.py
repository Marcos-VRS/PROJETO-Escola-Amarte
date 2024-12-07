import pandas as pd
from django.http import JsonResponse


def resumo_dados(request):
    file_path = r"C:\Users\Marcos\Desktop\PROJETO - Amarte\tabela_faker_dashboards.xlsx"

    # Tente carregar o arquivo
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    # Processar as colunas necessárias
    receitas = df[["Nome da Transação", "Receita"]].dropna()
    despesas = df[["Nome da Transação", "Despesa"]].dropna()

    resumo_receitas = receitas.to_dict(orient="records")
    resumo_despesas = despesas.to_dict(orient="records")

    return JsonResponse(
        {"resumo_receitas": resumo_receitas, "resumo_despesas": resumo_despesas}
    )
