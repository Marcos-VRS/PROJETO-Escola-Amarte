from django.shortcuts import render, redirect, get_object_or_404
from financeiro.forms import FinanceiroCadastroForm
from django.contrib.auth.decorators import login_required
from ..models import Financeiro_Cadastro


@login_required(login_url="financeiro:tela_login")
def criar_cadastro_view(request):
    username = request.user.username  # Obtém o nome de usuário do request

    if request.method == "POST":
        form = FinanceiroCadastroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("financeiro:cadastro")  # Redireciona após sucesso
    else:
        form = FinanceiroCadastroForm()

    return render(
        request,
        "global/partials/criar_cadastro.html",
        {"form": form, "username": username},
    )


@login_required(login_url="financeiro:tela_login")
def pesquisar_cadastro(request):
    username = request.user.username  # Obtém o nome de usuário do request
    query = request.GET.get("q", "")
    if query:
        resultados = (
            Financeiro_Cadastro.objects.filter(nome__icontains=query)
            | Financeiro_Cadastro.objects.filter(cpf_cnpj_numero__icontains=query)
            | Financeiro_Cadastro.objects.filter(email__icontains=query)
            | Financeiro_Cadastro.objects.filter(telefone__icontains=query)
            | Financeiro_Cadastro.objects.filter(categoria__name__icontains=query)
        )
    else:
        resultados = Financeiro_Cadastro.objects.all()

    return render(
        request,
        "global/partials/cadastro.html",
        {"resultados": resultados, "username": username},
    )


@login_required(login_url="financeiro:tela_login")
def atualizar_cadastro_view(request, id):  # Alterado para 'id'
    username = request.user.username  # Obtém o nome de usuário do request
    cadastro = get_object_or_404(Financeiro_Cadastro, id=id)  # Usando 'id' aqui também

    if request.method == "POST":
        form = FinanceiroCadastroForm(request.POST, request.FILES, instance=cadastro)
        if form.is_valid():
            form.save()
            return redirect("financeiro:cadastro")  # Redireciona após sucesso
    else:
        form = FinanceiroCadastroForm(instance=cadastro)

    return render(
        request,
        "global/partials/atualizar_cadastro.html",
        {"form": form, "username": username, "cadastro": cadastro},
    )
