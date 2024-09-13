from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Evento, Participante, Financeiro_Cadastro, Category
from ..forms import EventoForm
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import json


@login_required(login_url="financeiro:tela_login")
def calendario_view(request):
    username = request.user.username
    hoje = datetime.now().date()
    eventos = Evento.objects.all()

    return render(
        request,
        "calendario.html",
        {"hoje": hoje, "eventos": eventos, "username": username},
    )


@login_required(login_url="financeiro:tela_login")
def criar_evento(request):
    username = request.user.username
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            participantes_data = request.POST.get("participantes_selecionados")

            if participantes_data:
                try:
                    participantes = json.loads(
                        participantes_data
                    )  # Converte a string JSON em uma lista de dicionários
                    evento.participantes_selecionados = (
                        participantes  # Salva a lista como JSON no modelo
                    )
                    evento.save()  # Salvar o evento após adicionar participantes
                except json.JSONDecodeError:
                    # Opcional: lidar com o erro se a decodificação JSON falhar
                    pass

            return redirect("financeiro:eventos")
    else:
        form = EventoForm()

    return render(
        request,
        "global/partials/criar_evento.html",
        {"form": form, "username": username},
    )


@login_required(login_url="financeiro:tela_login")
def consultar_evento(request):
    username = request.user.username
    query_nome = request.GET.get("nome", "")
    query_data = request.GET.get("data", "")
    query_participante = request.GET.get("participante", "")
    eventos = Evento.objects.all()

    # Filtrar por nome do evento
    if query_nome:
        eventos = eventos.filter(nome__icontains=query_nome)

    # Filtrar por data do evento
    if query_data:
        try:
            # Certifique-se de que o campo de data está no formato correto
            data_obj = parse_date(query_data)
            if data_obj:
                eventos = eventos.filter(data=data_obj)
        except ValueError:
            pass

    # Filtrar por participante
    if query_participante:
        eventos = eventos.filter(
            participantes_selecionados__icontains=query_participante
        )

    context = {
        "eventos": eventos,
        "query_nome": query_nome,
        "query_data": query_data,
        "query_participante": query_participante,
        "username": username,
    }

    return render(
        request,
        "global/partials/consultar_evento.html",
        context,
    )


@login_required(login_url="financeiro:tela_login")
def buscar_participantes(request):
    categoria_nome = request.GET.get("categoria")
    print(f"Categoria recebida: {categoria_nome}")
    if categoria_nome:
        try:
            categoria = Category.objects.get(name=categoria_nome)
            print(f"achei a categoria {categoria_nome}")
            participantes = Financeiro_Cadastro.objects.filter(categoria=categoria)
            participantes_data = [
                {
                    "id": p.id,
                    "nome": p.nome,
                    "cpf": p.cpf_cnpj_numero,
                    "categoria": categoria_nome,
                }
                for p in participantes
            ]
            return JsonResponse({"participantes": participantes_data})
        except Category.DoesNotExist:
            print("não encontrei a categoria {categoria_nome}")
            return JsonResponse({"error": "Categoria não encontrada"}, status=404)
    else:
        return JsonResponse({"error": "Categoria não informada"}, status=400)


@login_required(login_url="financeiro:tela_login")
def listar_categorias(request):
    categorias = Category.objects.values_list("name", flat=True)
    return JsonResponse({"categorias": categorias})


@login_required(login_url="financeiro:tela_login")
def buscar_categorias(request):
    categorias = Category.objects.all()
    categorias_data = [{"nome": c.name} for c in categorias]
    return JsonResponse({"categorias": categorias_data})


@login_required(login_url="financeiro:tela_login")
def atualizar_evento(request, id):
    username = request.user.username
    evento = get_object_or_404(Evento, id=id)

    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect("financeiro:eventos")
    else:
        form = EventoForm(instance=evento)

    return render(
        request,
        "global/partials/atualizar_evento.html",
        {"form": form, "evento": evento, "username": username},
    )


def calendario_view(request):
    partial = request.GET.get("partial")
    today = timezone.now().date()  # Obtém a data de hoje

    if partial == "calendario_semanal.html":
        # Calcula o início e o fim da semana atual
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)

        # Obtém eventos que ocorrem na semana atual
        eventos = Evento.objects.filter(data__range=[start_of_week, end_of_week])

        # Cria uma lista de dias da semana para o calendário
        days = [start_of_week + timezone.timedelta(days=i) for i in range(7)]

        context = {
            "days": days,
            "today": today,
            "eventos": eventos,
        }
        return render(request, "global/partials/calendario_semanal.html", context)

    elif partial == "calendario_mensal.html":
        return render(request, "global/partials/calendario_mensal.html")

    else:
        return HttpResponse(status=404)
