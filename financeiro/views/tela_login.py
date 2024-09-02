from django.shortcuts import render, redirect
from financeiro.forms import RegisterUpdateForm
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, "Logado com sucesso")
            return redirect("financeiro:index")
            print(user)

        messages.error(request, "Login inválido")

    return render(request, "financeiro/tela_login.html", {"form": form})


@login_required(login_url="financeiro:tela_login")
def logout_view(request):
    auth.logout(request)
    return redirect("financeiro:tela_login")


@login_required(login_url="financeiro:tela_login")
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method == "POST":
        form = RegisterUpdateForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Alteração realizada com sucesso")
            return redirect("financeiro:index")

    return render(request, "financeiro/user_update.html", {"form": form})
