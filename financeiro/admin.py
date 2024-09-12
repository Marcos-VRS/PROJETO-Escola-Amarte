from django.contrib import admin
from financeiro.models import Financeiro_Cadastro, Category, Evento, Participante


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
        "categoria__name",  # Pesquisa pelo nome da categoria
    )
    list_per_page = 50
    list_max_show_all = 200
    list_display_links = (
        "id",
        "nome",
    )
    search_fields = ("nome", "cpf_cnpj_numero")  # Corrigido o campo "cpf"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("-id",)


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "categoria")  # Corrigido para corresponder ao modelo
    search_fields = ("nome", "cpf", "categoria")


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "data",
        "descricao",  # Corrigido o nome do campo para 'descricao'
    )
    search_fields = ("nome", "descricao")
    list_filter = ("data",)

    # Se você tiver campos ManyToMany ou ForeignKey, use autocomplete_fields para eles
    # autocomplete_fields = ("participantes",)

    # Adiciona autocomplete para campos ManyToMany
    autocomplete_fields = ("participantes",)
