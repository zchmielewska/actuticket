import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from ticket import forms, models
from ticket.utils.utils import send_mail_to_all


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        tickets = models.Ticket.objects.all()

        paginator = Paginator(tickets, 15)
        page = request.GET.get("page")

        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)

        return render(request, "ticket/main.html", {"page": page, "tickets": tickets})


class AddTicketView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.TicketForm
        return render(request, "ticket/ticket_form.html", {"form": form})

    def post(self, request):
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.created_at = datetime.datetime.now()
            ticket.save()
            form.save_m2m()

            # Inform users
            subject = f"New ticket {ticket.id}"
            message = f"{ticket.created_by.first_name} {ticket.created_by.last_name} has created a new ticket " \
                      f"{ticket.id}."
            send_mail_to_all(subject, message, "user@example.com")

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

        # Inform users
        subject = f"Ticket {ticket.id} is undertaken"
        message = f"{ticket.undertook_by.first_name} {ticket.undertook_by.last_name} undertook ticket {ticket.id}."
        send_mail_to_all(subject, message, "user@example.com")

        return redirect("ticket_detail", ticket.id)


class CloseTicketView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket.closed_by = request.user
        ticket.closed_at = datetime.datetime.now()
        ticket.status = 3
        ticket.save()

        # Inform users
        subject = f"Ticket {ticket.id} is closed"
        message = f"{ticket.closed_by.first_name} {ticket.closed_by.last_name} closed ticket {ticket.id}."
        send_mail_to_all(subject, message, "user@example.com")

        return redirect("ticket_detail", ticket.id)


class AddCommentView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        form = forms.CommentForm
        return render(request, "ticket/comment_form.html", {"form": form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form = forms.CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.written_by = request.user
            comment.written_at = datetime.datetime.now()
            comment.ticket = ticket
            comment.save()

            # Inform users
            subject = f"New comment for ticket {ticket.id}"
            message = f"{comment.written_by} {comment.written_at} added comment to ticket {ticket.id}."
            send_mail_to_all(subject, message, "user@example.com")

            return redirect("ticket_detail", ticket.id)
        return redirect("main", ticket.id)
