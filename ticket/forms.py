from django import forms

from ticket import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ("title", "model", "type", "version", "year", "month", "deadline", "information")
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "model": forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            "title": "e.g. sensitivities or proxy",
            "information": "e.g. path to the zip file with assumptions",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("message", )
