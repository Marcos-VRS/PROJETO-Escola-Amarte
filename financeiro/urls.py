from financeiro import views
from django.urls import path

app_name = "financeiro"

urlpatterns = [
    # User
    path("login/", views.tela_login.login_view, name="tela_login"),
    path("logout/", views.tela_login.logout_view, name="tela_logout"),
    path("update/", views.tela_login.user_update, name="user_update"),
    # index
    path("index/", views.index.index, name="index"),
]
