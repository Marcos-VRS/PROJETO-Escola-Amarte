# **PROJETO-Escola-Amarte**  

[![Django Version](https://img.shields.io/badge/Django-5.1.2-green)](https://www.djangoproject.com/) [![Python Version](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)  

Um sistema completo para a gestão de escolas de música, desenvolvido em **Python** com o framework **Django**.  
O projeto conta com:  
- Uma **landing page** para apresentar a escola e atrair alunos.  
- Um **sistema interno** que oferece recursos de gerenciamento financeiro, organização de agenda, armazenamento de dados e análise.  

---

## **Tabela de Conteúdo**

1. [Recursos](#recursos)  
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)  
3. [Instalação](#instalação)  
4. [Uso](#uso)  
5. [Contribuição](#contribuição)  
6. [Licença](#licença)  

---

## **Recursos**  

### **Landing Page (App `site`)**  
- Página inicial interativa para apresentar a escola.  
- Foco em design intuitivo e atraente para novos visitantes.  

### **Sistema Interno (App `programa`)**  
- **Banco de Dados**: Cadastro de alunos, professores e eventos.  
- **Calendário Dinâmico**: Organização de aulas, eventos e compromissos.  
- **Gerenciamento Financeiro**: Controle de receitas e despesas.  
- **Análise de Dados**: Geração de relatórios para tomada de decisão.  
- **Agenda Escolar**: Ferramenta para otimizar a organização da escola.  

---

## **Tecnologias Utilizadas**  

- **Frontend:** HTML, CSS, JavaScript.  
- **Backend:** Django 5.1.2, Python 3.11.  
- **Banco de Dados:** SQLite (configuração padrão, personalizável).  
- **Bibliotecas e Dependências:**  
  - [Pandas](https://pandas.pydata.org/) para análise de dados.  
  - [OpenPyxl](https://openpyxl.readthedocs.io/) para manipulação de planilhas Excel.  
  - [Django Import Export](https://django-import-export.readthedocs.io/) para importação/exportação de dados.  
  - [Faker](https://faker.readthedocs.io/) para geração de dados fictícios.  

---

## **Instalação**  

### **Pré-requisitos**  
- Python 3.11 ou superior.  
- Pip instalado.  

### **Passos para Instalação**  
1. Clone o repositório:  
   ```bash
   git clone https://github.com/Marcos-VRS/PROJETO-Escola-Amarte.git
   cd PROJETO-Escola-Amarte
2. Crie e ative um ambiente virtual:
   python -m venv venv  
   source venv/bin/activate  # Linux/Mac  
   venv\Scripts\activate     # Windows
3. Instale as dependências:
   pip install -r requirements.txt
4.Execute as migrações:
  python manage.py migrate
5.Inicie o servidor:
   python manage.py runserver  

---

## **Uso**
- Acesse o sistema na URL: http://127.0.0.1:8000/.
- Landing Page: Página inicial acessível por todos os usuários.
- Sistema Interno: Necessita login (crie um superusuário com python manage.py createsuperuser).

---

## **Contribuição**

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch com sua funcionalidade ou correção:
   git checkout -b minha-contribuicao  
3. Envie um Pull Request para revisão.

---

## **Licença**

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.


## **Contato**

-Desenvolvedor: Marcos-VRS
-Email: marcosvrsdevmail@gmail.com
-LinkedIn: https://www.linkedin.com/in/marcos-vin%C3%ADcius-ramos-da-silva-557b18a5/







