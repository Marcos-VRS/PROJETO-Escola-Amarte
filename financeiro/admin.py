from django.contrib import admin
from financeiro.models import Financeiro_Cadastro, Category, Evento


@admin.register(Financeiro_Cadastro)
class FinanceiroCadastroAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "telefone",
        "email",
        "data_de_criação",
        "descrição",
        "categoria",
    )
    ordering = ("-id",)
    search_fields = (
        "id",
        "nome",
        "categoria",
    )
    list_per_page = 50
    list_max_show_all = 200
    list_display_links = (
        "id",
        "nome",
    )

    # Adiciona autocomplete para campos de busca
    search_fields = ("nome", "cpf")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("-id",)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "data",
        "hora",
        "descrição",
    )
    search_fields = ("nome", "descrição")
    filter_horizontal = (
        "professores",
        "alunos",
    )
    list_filter = ("data", "hora")

    # Adiciona autocomplete para campos ManyToMany
    autocomplete_fields = ("professores", "alunos")
