from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="financeiro:tela_login")
def index(request):
    return render(request, "financeiro/index.html", {"username": request.user.username})


@login_required(login_url="financeiro:tela_login")
def dashboard(request):
    return render(
        request, "financeiro/dashboard.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def transacoes(request):
    return render(
        request, "financeiro/transacoes.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def aulas(request):
    return render(request, "financeiro/aulas.html", {"username": request.user.username})


@login_required(login_url="financeiro:tela_login")
def cadastro(request):
    return render(
        request, "financeiro/cadastro.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def fiscal(request):
    return render(
        request, "financeiro/fiscal.html", {"username": request.user.username}
    )


@login_required(login_url="financeiro:tela_login")
def metas(request):
    return render(request, "financeiro/metas.html", {"username": request.user.username})
