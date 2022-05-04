from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View

from ticket import forms, models
from .tasks import send_mail_to_all


class MainView(LoginRequiredMixin, View):
    """Main page of the app with the list of new tickets."""
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
    """
    Form to add a new ticket.

    The form uses save_m2m() because it has many-to-many relationship with models.
    The users are informed about the new ticket by e-mail (using celery to avoid long waiting time).
    """
    def get(self, request):
        form = forms.TicketForm
        return render(request, "ticket/ticket_form.html", {"form": form})

    def post(self, request):
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.created_at = timezone.now()
            ticket.save()
            form.save_m2m()

            # Inform users
            subject = f"actuticket | new ticket {ticket.id}"
            message = f"{ticket.created_by.first_name} {ticket.created_by.last_name} has created a new ticket " \
                      f"{ticket.id}."
            send_mail_to_all.delay(subject, message)

            return redirect(reverse_lazy("main"))
        return render(request, "ticket/ticket_form.html", {"form": form})


class TicketDetailView(LoginRequiredMixin, View):
    """View with ticket's details."""
    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        return render(request, "ticket/ticket_detail.html", {"ticket": ticket})


class UndertakeTicketView(LoginRequiredMixin, View):
    """View to undertake ticket."""
    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket.undertook_by = request.user
        ticket.undertook_at = timezone.now()
        ticket.status = 2
        ticket.save()

        # Inform users
        subject = f"actuticket | ticket {ticket.id} is undertaken"
        message = f"{ticket.undertook_by.first_name} {ticket.undertook_by.last_name} undertook ticket {ticket.id}."
        send_mail_to_all.delay(subject, message)

        return redirect("ticket_detail", ticket.id)


class CloseTicketView(LoginRequiredMixin, View):
    """View to close ticket."""
    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if ticket.status != 2:
            return redirect("ticket_detail", ticket.id)

        ticket.closed_by = request.user
        ticket.closed_at = timezone.now()
        ticket.status = 3
        ticket.save()

        # Inform users
        subject = f"actuticket | ticket {ticket.id} is closed"
        message = f"{ticket.closed_by.first_name} {ticket.closed_by.last_name} closed ticket {ticket.id}."
        send_mail_to_all.delay(subject, message)

        return redirect("ticket_detail", ticket.id)


class AddCommentView(LoginRequiredMixin, View):
    """Form to add comment to a ticket."""
    def get(self, request, ticket_id):
        form = forms.CommentForm
        return render(request, "ticket/comment_form.html", {"form": form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form = forms.CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.written_by = request.user
            comment.written_at = timezone.now()
            comment.ticket = ticket
            comment.save()

            # Inform users
            subject = f"actuticket | new comment for ticket {ticket.id}"
            message = f"{comment.written_by} added comment to ticket {ticket.id}."
            send_mail_to_all.delay(subject, message)

            return redirect("ticket_detail", ticket.id)
        return redirect("main", ticket.id)
