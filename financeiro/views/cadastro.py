from django.shortcuts import render, redirect
from financeiro.forms import FinanceiroCadastroForm
from django.contrib.auth.decorators import login_required


@login_required(login_url="financeiro:tela_login")
def criar_cadastro_view(request):
    if request.method == "POST":
        form = FinanceiroCadastroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(
                "financeiro:cadastro"
            )  # Redireciona para a lista de cadastros ou outra página após o sucesso
    else:
        form = FinanceiroCadastroForm()
    return render(request, "global/partials/criar_cadastro.html", {"form": form})
