from django.shortcuts import render
from site_amarte.forms import RegisterForm


def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

    return render(request, "site_amarte/register.html", {"form": form})
