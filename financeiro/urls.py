from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from financeiro import views

app_name = "financeiro"

urlpatterns = [
    # User
    path("login/", views.tela_login.login_view, name="tela_login"),
    path("logout/", views.tela_login.logout_view, name="tela_logout"),
    # Menu lateral
    path("index/", views.index.index_financeiro, name="index"),
    path("dashboard/", views.index.dashboard, name="dashboard"),
    path("transacoes/", views.index.transacoes, name="transacoes"),
    path("eventos/", views.index.eventos, name="eventos"),
    path("cadastro/", views.index.cadastro, name="cadastro"),
    path("fiscal/", views.index.fiscal, name="fiscal"),
    path("metas/", views.index.metas, name="metas"),
    path("tarefas/", views.index.tarefas, name="tarefas"),
    # CRUD - CADASTRO
    path("cadastro/criar/", views.cadastro.criar_cadastro_view, name="criar_cadastro"),
    path("pesquisar/", views.cadastro.pesquisar_cadastro, name="pesquisar_cadastro"),
    path(
        "atualizar/<int:id>/",
        views.cadastro.atualizar_cadastro_view,
        name="atualizar_cadastro",
    ),
    # CRUD - EVENTOS
    path("criar_evento/", views.eventos.criar_evento, name="criar_evento"),
    path("evento/consultar/", views.eventos.consultar_evento, name="consultar_evento"),
    path(
        "atualizar/evento/<int:id>/",
        views.eventos.atualizar_evento,
        name="atualizar_evento",
    ),
    path(
        "buscar_participantes/",
        views.eventos.buscar_participantes,
        name="buscar_participantes",
    ),
    path(
        "buscar-categorias/", views.eventos.buscar_categorias, name="buscar_categorias"
    ),
    path("eventos/calendario/", views.eventos.calendario_view, name="calendario_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
