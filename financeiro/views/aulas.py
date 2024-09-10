from django.shortcuts import render, redirect
from ..models import Evento
from ..forms import EventoForm
from datetime import datetime


def calendario_view(request):
    hoje = datetime.now().date()
    eventos = Evento.objects.all()

    return render(
        request,
        "calendario.html",
        {"hoje": hoje, "eventos": eventos},
    )


def adicionar_evento(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("calendario:calendario")
    else:
        form = EventoForm()

    return render(request, "adicionar_evento.html", {"form": form})
