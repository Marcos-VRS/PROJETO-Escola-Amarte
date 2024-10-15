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


class MeuCalendario(HTMLCalendar):
    def __init__(self, eventos):
        super().__init__()
        self.eventos = eventos
        self.setfirstweekday(SUNDAY)  # Definir o domingo como o primeiro dia da semana

    def primeiro_e_ultimo_dia_da_semana(self, ano, mes):
        """
        Calcula o primeiro e o último dia da semana a partir da data fornecida.
        """
        primeira_data = datetime(ano, mes, 1)  # Primeira data do mês

        primeiro_dia = primeira_data - timedelta(
            days=primeira_data.weekday()
        )  # Domingo anterior
        ultimo_dia = primeiro_dia + timedelta(days=6)  # Sábado da mesma semana
        return primeiro_dia, ultimo_dia

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
                    semana.append({"numero_dia": day, "eventos": eventos_do_dia})
                else:
                    semana.append({"numero_dia": None, "eventos": []})

            calendario.append(semana)

        return calendario

    def eventos_para_dicionarios_semana(self, ano, mes):
        # Criar um calendário e obter as semanas com datas completas (dia, mês, ano)
        cal = calendar.Calendar()
        semanas = cal.monthdatescalendar(ano, mes)

        # for semana in semanas:
        #     print(f"Aqui estão as semanas: {semana}")

        calendario = []

        for semana in semanas:
            semana_completa = []
            for dia in semana:
                # Filtrar os eventos para o dia atual
                eventos_do_dia = [
                    {
                        "nome": evento.nome,
                        "hora": evento.hora.strftime("%H:%M"),
                        "duracao": evento.duracao,
                        "data": evento.data.strftime("%Y-%m-%d"),
                        "descricao": evento.descricao,
                        "participantes": [
                            {
                                "nome": participante["nome"],
                                "categoria": participante["categoria"],
                            }
                            for participante in evento.participantes_selecionados
                        ],
                    }
                    for evento in self.eventos
                    if evento.data.day == dia.day
                    and evento.data.month == dia.month
                    and evento.data.year == dia.year
                ]

                semana_completa.append(
                    {
                        "numero_dia": dia.day,
                        "mes": dia.month,
                        "ano": dia.year,
                        "eventos": eventos_do_dia,
                    }
                )

            calendario.append(semana_completa)

        # for calendarios in calendario:
        #     print(f"Aqui está o calendário : {calendarios}")

        return calendario


def dias_da_semana_atual(hoje):
    # Obter o primeiro dia da semana (domingo)
    primeiro_dia_semana = hoje - timedelta(days=hoje.weekday() + 1)
    dias_semana = []

    for i in range(7):  # De domingo a sábado
        dia_atual = primeiro_dia_semana + timedelta(days=i)

        dias_semana.append(
            {"numero_dia": dia_atual.day, "mes": dia_atual.month, "ano": dia_atual.year}
        )
    return dias_semana


@login_required(login_url="financeiro:tela_login")
def calendario_view(request, periodo, ano=None, mes=None):
    username = request.user.username
    hoje = datetime.now()  # Data atual
    semana_atual = dias_da_semana_atual(hoje)

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

    # Navegação das semanas
    mes_anterior = hoje.replace(
        month=mes - 1 if mes > 1 else 12, year=ano - 1 if mes == 1 else ano
    )
    mes_seguinte = hoje.replace(
        month=mes + 1 if mes < 12 else 1, year=ano + 1 if mes == 12 else ano
    )

    # Navegação dos meses
    semana_anterior = hoje - timedelta(days=7)
    semana_seguinte = hoje + timedelta(days=7)

    # Nome do mês baseado no número
    nome_mes = nomes_meses[mes - 1]

    # Consultar os eventos do mês/ano fornecidos
    eventos = Evento.objects.filter(data__year=ano, data__month=mes)

    # Definir variáveis para o calendário
    calendario = None

    if periodo == "mensal":
        # Exibir o calendário mensal
        calendario = MeuCalendario(eventos).eventos_para_dicionarios(ano, mes)
        partial = "global/partials/calendario_mensal.html"

    if periodo == "semanal":
        # Exibir o calendário mensal

        calendario = MeuCalendario(eventos).eventos_para_dicionarios_semana(ano, mes)
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
            "semana_atual": semana_atual,
            "nome_mes": nome_mes,
            "ano": ano,
            "mes_anterior": mes_anterior,
            "mes_seguinte": mes_seguinte,
            "semana_anterior": semana_anterior,
            "semana_seguinte": semana_seguinte,
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

            # Adicionar lógica de recorrência
            recorrencia = form.cleaned_data.get("recorrência")
            numero_repeticoes = form.cleaned_data.get(
                "repetições"
            )  # Obter o valor de repeticoes do formulário

            if recorrencia in ["Semanal", "Mensal"] and numero_repeticoes > 1:
                for i in range(1, numero_repeticoes + 1):
                    if recorrencia == "Semanal":
                        nova_data = evento.data + timedelta(weeks=i)
                    elif recorrencia == "Mensal":
                        nova_data = evento.data + relativedelta(
                            months=i
                        )  # Usa months para adicionar meses

                    novo_evento = Evento(
                        nome=evento.nome,
                        data=nova_data,
                        hora=evento.hora,
                        duracao=evento.duracao,
                        descricao=evento.descricao,
                        recorrência=evento.recorrência,
                        participantes_selecionados=evento.participantes_selecionados,
                    )
                    novo_evento.save()

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


@login_required(login_url="financeiro:tela_login")
def buscar_participantes(request):
    categoria_nome = request.GET.get("categoria")
    if categoria_nome:
        try:
            categoria = Category.objects.get(name=categoria_nome)
            participantes = Financeiro_Cadastro.objects.filter(categoria=categoria)
            participantes_data = [
                {
                    "id": p.id,
                    "nome": p.nome,
                    "cpf": p.cpf_cnpj_numero,
                    "categoria": categoria_nome,
                    "email": p.email,
                    "telefone": p.telefone,
                    "descricao": p.descrição,
                    "cpf_cnpj_tipo": p.cpf_cnpj_tipo,
                    "cpf_cnpj_numero": p.cpf_cnpj_numero,
                    "categoria_de_pagamento": p.categoria_de_pagamento,
                    "frequencia_de_pagamento": p.frequencia_de_pagamento,
                    "data_de_pagamento": p.data_de_pagamento,
                    "valor_pago": p.valor_pago,
                }
                for p in participantes
            ]
            for a in participantes_data:
                print(f"Aqui estão so dados dos participantes:{participantes_data}")
            return JsonResponse({"participantes": participantes_data})
        except Category.DoesNotExist:
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

    # Carregar os participantes selecionados (JSON)
    participantes_json = evento.participantes_selecionados
    participantes_lista = []

    # Tratar o JSON para extrair nome e categoria
    for participante in participantes_json:
        nome = participante.get("nome", "Nome Desconhecido")
        categoria = participante.get("categoria", "Categoria Desconhecida")
        participantes_lista.append(f"{nome} ({categoria})")

    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
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
        form = EventoForm(instance=evento)

    return render(
        request,
        "global/partials/atualizar_evento.html",
        {
            "form": form,
            "evento": evento,
            "username": username,
            "participantes_lista": participantes_lista,
        },
    )
