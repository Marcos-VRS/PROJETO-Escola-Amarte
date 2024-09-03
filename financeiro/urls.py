from financeiro import views
from django.urls import path

app_name = "financeiro"

urlpatterns = [
    # User
    path("login/", views.tela_login.login_view, name="tela_login"),
    path("logout/", views.tela_login.logout_view, name="tela_logout"),
    # Menu lateral
    path("dashboard/", views.index.dashboard, name="dashboard"),
]
