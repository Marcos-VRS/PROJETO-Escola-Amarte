from django.urls import path
from site_amarte import views


app_name = "site_amarte"


urlpatterns = [
    path("", views.index, name="index"),
    # User
    path("user/create/", views.register, name="register"),
]
