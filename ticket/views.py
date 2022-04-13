from django.shortcuts import render
from django.views import View

from ticket import forms


class MainView(View):
    def get(self, request):
        return render(request, "ticket/main.html")


class AddTicketView(View):
    def get(self, request):
        form = forms.TicketForm
        return render(request, "ticket/ticket_form.html", {"form": form})
