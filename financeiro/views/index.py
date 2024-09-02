from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="financeiro:tela_login")
def index(request):
    return render(request, "financeiro/index.html")
