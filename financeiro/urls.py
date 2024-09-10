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
    path("aulas/", views.index.aulas, name="aulas"),
    path("cadastro/", views.index.cadastro, name="cadastro"),
    path("fiscal/", views.index.fiscal, name="fiscal"),
    path("metas/", views.index.metas, name="metas"),
    path("tarefas/", views.index.tarefas, name="tarefas"),
    # CRUD
    path("cadastro/criar/", views.cadastro.criar_cadastro_view, name="criar_cadastro"),
    path("pesquisar/", views.cadastro.pesquisar_cadastro, name="pesquisar_cadastro"),
    path(
        "atualizar/<int:id>/",
        views.cadastro.atualizar_cadastro_view,
        name="atualizar_cadastro",
    ),
    # Aulas
    path("evento/criar", views.aulas.criar_evento, name="criar_evento"),
    path("evento/consultar", views.aulas.consultar_evento, name="consultar_evento"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
