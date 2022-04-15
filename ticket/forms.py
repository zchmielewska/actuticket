from django import forms

from ticket import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ("model", "type", "version", "year", "month", "deadline")
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }
