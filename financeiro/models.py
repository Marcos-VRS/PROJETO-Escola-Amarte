from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name}"


class Financeiro_Cadastro(models.Model):
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    data_de_criação = models.DateTimeField(default=timezone.now)
    descrição = models.TextField()
    categoria = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.nome} "
