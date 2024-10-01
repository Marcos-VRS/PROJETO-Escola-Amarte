from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re


# Modelo para Categoria
class Category(models.Model):
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name}"


# Modelo para Cadastro Financeiro
class Financeiro_Cadastro(models.Model):
    class Meta:
        verbose_name = "Cadastro"
        verbose_name_plural = "Cadastro"

    CPF_CNPJ_CHOICES = [
        ("CPF", "CPF"),
        ("CNPJ", "CNPJ"),
    ]

    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    data_de_criação = models.DateTimeField(default=timezone.now)
    descrição = models.TextField()
    categoria = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    cpf_cnpj_tipo = models.CharField(
        max_length=4, choices=CPF_CNPJ_CHOICES, default="CPF"
    )
    cpf_cnpj_numero = models.CharField(max_length=20, blank=False)

    def __str__(self) -> str:
        return f"{self.nome}"

    def clean(self):
        super().clean()
        if not self.email or not self.validar_email(self.email):
            raise ValidationError("Digite um endereço de e-mail válido.")
        if self.cpf_cnpj_tipo == "CPF":
            if not self.validar_cpf(self.cpf_cnpj_numero):
                raise ValidationError("Número de CPF inválido.")
        elif self.cpf_cnpj_tipo == "CNPJ":
            if not self.validar_cnpj(self.cpf_cnpj_numero):
                raise ValidationError("Número de CNPJ inválido.")

    def validar_email(self, email):
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(regex, email) is not None

    def validar_cpf(self, cpf):
        cpf = re.sub(r"\D", "", cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        def calcular_digitos(cpf):
            soma = 0
            for i in range(9):
                soma += int(cpf[i]) * (10 - i)
            digito1 = 11 - (soma % 11)
            digito1 = 0 if digito1 > 9 else digito1
            soma = 0
            for i in range(10):
                soma += int(cpf[i]) * (11 - i)
            digito2 = 11 - (soma % 11)
            digito2 = 0 if digito2 > 9 else digito2
            return str(digito1) + str(digito2)

        return cpf[-2:] == calcular_digitos(cpf)

    def validar_cnpj(self, cnpj):
        cnpj = re.sub(r"\D", "", cnpj)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        def calcular_digitos(cnpj):
            def soma_digitos(cnpj, pesos):
                return sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))

            pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            pesos2 = [6] + pesos1
            soma1 = soma_digitos(cnpj, pesos1)
            digito1 = 11 - (soma1 % 11)
            digito1 = 0 if digito1 > 9 else digito1
            soma2 = soma_digitos(cnpj, pesos2)
            digito2 = 11 - (soma2 % 11)
            digito2 = 0 if digito2 > 9 else digito2
            return str(digito1) + str(digito2)

        return cnpj[-2:] == calcular_digitos(cnpj)


# Modelo para Participante
class Participante(models.Model):
    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"

    CATEGORIA_CHOICES = [
        ("professores", "Professores"),
        ("alunos", "Alunos"),
        ("fornecedores", "Fornecedores"),
        ("outros", "Outros"),
    ]

    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

    @staticmethod
    def buscar_por_categoria(categoria):
        return Financeiro_Cadastro.objects.filter(categoria__name=categoria).values(
            "nome", "cpf_cnpj_numero"
        )


# modelo Evento
class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField()
    duracao = models.CharField(max_length=100)  # Campo para Duração
    descricao = models.TextField()
    participantes = models.ManyToManyField(Participante, blank=True)
    participantes_selecionados = models.JSONField(default=dict, blank=True)

    # outros campos e métodos

    def __str__(self):
        return self.nome
