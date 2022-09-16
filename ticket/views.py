from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.views import View

from ticket import forms, models
from .tasks import send_mail_to_all
from ticket.utils import utils


DOMAIN = settings.DEFAULT_DOMAIN


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
        initial_dict = {
            "model": models.Model.objects.all()
        }

        form = forms.TicketForm(initial=initial_dict)
        return render(request, "ticket/ticket_form.html", {"form": form})

    def post(self, request):
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.created_at = timezone.now()
            ticket.save()
            form.save_m2m()

            # Show success message
            messages.success(request, f"You have added ticket #{ticket.id}")

            # Inform users by e-mail
            subject = f"actuticket | new ticket {ticket.id} ({ticket.title})"
            ctx = {"ticket": ticket, "domain": DOMAIN}
            html_message = render_to_string("email/add-ticket.html", ctx)
            plain_message = strip_tags(html_message)
            send_mail_to_all.delay(subject, plain_message, html_message)

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

        # Show success message
        messages.success(request, f"You have undertaken ticket #{ticket.id}")

        # Inform users by e-mail
        subject = f"actuticket | ticket {ticket.id} ({ticket.title}) is undertaken"
        good_luck = utils.generate_good_luck()
        ctx = {"ticket": ticket, "good_luck": good_luck, "domain": DOMAIN}
        html_message = render_to_string("email/undertake-ticket.html", ctx)
        plain_message = strip_tags(html_message)
        send_mail_to_all.delay(subject, plain_message, html_message)

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

        # Show success message
        messages.success(request, f"You have closed ticket #{ticket.id}")

        # Inform users by e-mail
        subject = f"actuticket | ticket {ticket.id} ({ticket.title}) is closed"
        good_job = utils.generate_good_job()
        ctx = {"ticket": ticket, "good_job": good_job, "domain": DOMAIN}
        html_message = render_to_string("email/close-ticket.html", ctx)
        plain_message = strip_tags(html_message)
        send_mail_to_all.delay(subject, plain_message, html_message)

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

            # Show success message
            messages.success(request, f"You have commented ticket #{ticket.id}")

            # Inform users by e-mail
            subject = f"actuticket | ticket {ticket.id} ({ticket.title}) has new comment"
            ctx = {"comment": comment, "domain": DOMAIN}
            html_message = render_to_string("email/comment-ticket.html", ctx)
            plain_message = strip_tags(html_message)
            send_mail_to_all.delay(subject, plain_message, html_message)

            return redirect("ticket_detail", ticket.id)
        return redirect("main", ticket.id)
