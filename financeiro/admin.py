from django.contrib import admin
from financeiro.models import Financeiro_Cadastro
from financeiro.models import Category

# Register your models here.


@admin.register(Financeiro_Cadastro)
class ContactAdmin(admin.ModelAdmin):
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("-id",)
