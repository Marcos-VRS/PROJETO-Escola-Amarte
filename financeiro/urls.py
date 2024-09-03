from financeiro import views
from django.urls import path

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
]
