from django import forms
from .models import Financeiro_Cadastro
import re


class FinanceiroCadastroForm(forms.ModelForm):

    class Meta:
        model = Financeiro_Cadastro
        fields = [
            "nome",
            "telefone",
            "email",
            "descrição",
            "categoria",
            "cpf_cnpj_tipo",
            "cpf_cnpj_numero",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "descrição": forms.Textarea(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "cpf_cnpj_tipo": forms.Select(attrs={"class": "form-control"}),
            "cpf_cnpj_numero": forms.TextInput(attrs={"class": "form-control"}),
        }
