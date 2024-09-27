from django import forms
from .models import Financeiro_Cadastro, Evento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            "nome",
            "data",
            "hora",
            "duracao",
            "descricao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "hora": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "duracao": forms.TextInput(
                attrs={"placeholder": "Duração do evento (ex: 2 horas)"}
            ),
            "descricao": forms.Textarea(attrs={"class": "form-control"}),
        }


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
            "categoria": forms.Select(
                attrs={"class": "form-control"}
            ),  # Lista de opções
            "cpf_cnpj_tipo": forms.Select(attrs={"class": "form-control"}),
            "cpf_cnpj_numero": forms.TextInput(attrs={"class": "form-control"}),
        }
