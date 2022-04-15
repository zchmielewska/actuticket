import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from ticket import forms, models


class MainView(View):
    def get(self, request):
        tickets = models.Ticket.objects.all()
        return render(request, "ticket/main.html", {"tickets": tickets})


class AddTicketView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.TicketForm
        return render(request, "ticket/ticket_form.html", {"form": form})

    def post(self, request):
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            form.save_m2m()
            return redirect(reverse_lazy("main"))
        return render(request, "ticket/ticket_form.html", {"form": form})


class TicketDetailView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        return render(request, "ticket/ticket_detail.html", {"ticket": ticket})


class UndertakeTicketView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket.undertook_by = request.user
        ticket.undertook_at = datetime.datetime.now()
        ticket.status = 2
        ticket.save()
        return redirect("ticket_detail", ticket.id)


class CloseTicketView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket.closed_by = request.user
        ticket.closed_at = datetime.datetime.now()
        ticket.status = 3
        ticket.save()
        return redirect("ticket_detail", ticket.id)
