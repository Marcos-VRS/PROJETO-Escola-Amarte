from django.shortcuts import render, redirect
from ..models import Evento
from django.contrib.auth.decorators import login_required
from ..forms import EventoForm
from datetime import datetime
from django.utils.dateparse import parse_date  # Para converter string em objeto de data


@login_required(login_url="financeiro:tela_login")
def calendario_view(request):
    username = request.user.username  # Obtém o nome de usuário do request
    hoje = datetime.now().date()
    eventos = Evento.objects.all()

    return render(
        request,
        "calendario.html",
        {"hoje": hoje, "eventos": eventos, "username": username},
    )


@login_required(login_url="financeiro:tela_login")
def criar_evento(request):
    username = request.user.username  # Obtém o nome de usuário do request
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("calendario:calendario")
    else:
        form = EventoForm()

    return render(request, "criar_evento.html", {"form": form, "username": username})


@login_required(login_url="financeiro:tela_login")
def consultar_evento(request):
    username = request.user.username  # Obtém o nome de usuário do request
    query_nome = request.GET.get("nome")  # Pesquisa por nome
    query_data = request.GET.get("data")  # Pesquisa por data
    eventos = Evento.objects.all()  # Começa com todos os eventos

    # Filtro por nome, se fornecido
    if query_nome:
        eventos = eventos.filter(nome__icontains=query_nome)

    # Filtro por data, se fornecido e válido
    if query_data:
        try:
            # Tenta converter a string da data para um objeto datetime.date
            data_obj = parse_date(query_data)
            if data_obj:
                eventos = eventos.filter(data=data_obj)
        except ValueError:
            # Se a data for inválida, você pode tratar o erro ou ignorar
            pass

    context = {
        "eventos": eventos,
        "query_nome": query_nome,
        "query_data": query_data,
        "username": username,
    }

    return render(
        request,
        "global/partials/consultar_evento.html",
        context,
    )
