from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Evento, Participante, Financeiro_Cadastro, Category
from ..forms import EventoForm
from datetime import datetime, timedelta, date
from django.utils.dateparse import parse_date
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import json, calendar
from django.utils.html import format_html
from calendar import HTMLCalendar, SUNDAY
from dateutil.relativedelta import relativedelta


@login_required(login_url="financeiro:tela_login")
def consultar_evento_transacoes(request):
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

    # Ordenar eventos por data em ordem decrescente
    eventos = eventos.order_by("-data", "hora")

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
