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


class MeuCalendario(HTMLCalendar):
    def __init__(self, eventos):
        super().__init__()
        self.eventos = eventos
        self.setfirstweekday(SUNDAY)  # Definir o domingo como o primeiro dia da semana

    def formatday(self, day, weekday):
        """
        Customiza a renderização de um dia do calendário.
        day: o número do dia
        weekday: o número do dia da semana (domingo, segunda, etc.)
        """
        if day == 0:
            # Dias fora do mês
            return '<td class="noday"></td>'

        # Filtrar eventos do dia atual
        eventos_do_dia = [
            evento
            for evento in self.eventos
            if evento.data.day == day and evento.data.month == self.current_month
        ]

        # Template de HTML do quadro do dia
        dia_html = f'<div class="day-box"><h3>{day}</h3>'

        # Adicionar eventos do dia ao quadro
        if eventos_do_dia:
            dia_html += "<ul>"
            for evento in eventos_do_dia:
                # Usando evento.hora para mostrar a hora
                dia_html += f'<li>{evento.nome} - {evento.hora.strftime("%H:%M")} ({evento.duracao})</li>'
            dia_html += "</ul>"
        else:
            dia_html += "<p>Sem eventos</p>"

        dia_html += "</div>"

        return f'<td class="{self.cssclasses[weekday]}">{dia_html}</td>'

    def formatweek(self, theweek):
        """
        Customiza a renderização de uma semana.
        """
        week_html = "".join(self.formatday(day, weekday) for (day, weekday) in theweek)
        return f"<tr>{week_html}</tr>"

    def eventos_para_dicionarios(self, ano, mes):
        # Obter a estrutura do mês em semanas (7 dias por semana, com dias 0 para dias fora do mês)
        dias_do_mes = self.monthdays2calendar(ano, mes)
        calendario = []

        for week in dias_do_mes:
            semana = []
            for day, weekday in week:
                if day != 0:
                    # Filtrar os eventos para o dia atual
                    eventos_do_dia = [
                        {
                            "nome": evento.nome,
                            "hora": evento.hora.strftime("%H:%M"),
                            "duracao": evento.duracao,
                            "data": evento.data.strftime("%Y-%m-%d"),
                        }
                        for evento in self.eventos
                        if evento.data.day == day and evento.data.month == mes
                    ]
                    # Adiciona o dia com seus eventos
                    semana.append({"numero_dia": day, "eventos": eventos_do_dia})
                else:
                    # Se for 0 (dia fora do mês), adiciona um dia vazio
                    semana.append({"numero_dia": "", "eventos": []})
            calendario.append(semana)
        return calendario

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Customiza a renderização de um mês inteiro.
        """
        self.current_month = themonth  # Armazenar o mês atual
        calendar_html = (
            '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        )
        calendar_html += (
            f"{self.formatmonthname(theyear, themonth, withyear=withyear)}\n"
        )
        calendar_html += f"{self.formatweekheader()}\n"

        for week in self.monthdays2calendar(theyear, themonth):
            calendar_html += f"{self.formatweek(week)}\n"

        return calendar_html


@login_required(login_url="financeiro:tela_login")
def calendario_view(request, periodo, ano=None, mes=None):
    username = request.user.username
    hoje = datetime.now()  # Data atual

    # Lista de nomes dos meses
    nomes_meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    # Usar ano e mês passados na URL ou o mês/ano atuais
    if ano is None:
        ano = hoje.year
    if mes is None:
        mes = hoje.month

    # Navegação dos meses
    mes_anterior = hoje.replace(
        month=mes - 1 if mes > 1 else 12, year=ano - 1 if mes == 1 else ano
    )
    mes_seguinte = hoje.replace(
        month=mes + 1 if mes < 12 else 1, year=ano + 1 if mes == 12 else ano
    )

    # Nome do mês baseado no número
    nome_mes = nomes_meses[mes - 1]

    # Consultar os eventos do mês/ano fornecidos
    eventos = Evento.objects.filter(data__year=ano, data__month=mes)
    calendario = MeuCalendario(eventos).eventos_para_dicionarios(ano, mes)

    # Definindo o template parcial com base no período
    if periodo == "mensal":
        partial = "global/partials/calendario_mensal.html"
    elif periodo == "semanal":
        partial = "global/partials/calendario_semanal.html"

    # Renderizar o template com os dados
    return render(
        request,
        "global/partials/eventos.html",
        {
            "calendario": calendario,
            "username": username,
            "partial": partial,
            "hoje": hoje,
            "mes": mes,
            "nome_mes": nome_mes,
            "ano": ano,
            "mes_anterior": mes_anterior,
            "mes_seguinte": mes_seguinte,
        },
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
