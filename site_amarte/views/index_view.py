from django.shortcuts import render


# view da página principal
def index(request):
    print("página inicial")
    return render(request, "site_amarte/index.html")
