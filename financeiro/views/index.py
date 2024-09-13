from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="financeiro:tela_login")
def index_financeiro(request):
    return render(
        request, "global/index_financeiro.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def tarefas(request):
    return render(
        request, "global/partials/tarefas.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def dashboard(request):
    return render(
        request, "global/partials/dashboard.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def transacoes(request):
    return render(
        request, "global/partials/transacoes.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def eventos(request):
    return render(
        request, "global/partials/eventos.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def cadastro(request):
    return render(
        request, "global/partials/cadastro.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def fiscal(request):
    return render(
        request, "global/partials/fiscal.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def metas(request):
    return render(
        request, "global/partials/metas.html", {"username": request.user.username}
    )
