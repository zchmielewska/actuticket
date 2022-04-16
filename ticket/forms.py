from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from ticket import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ("model", "type", "version", "year", "month", "deadline", "information")
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "model": forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("message", )
