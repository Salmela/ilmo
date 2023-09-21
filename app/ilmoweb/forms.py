"""Module for forms."""
from django import forms

class NewLabForm(forms.Form):
    """
        Form for creating new labs.

    """
    name = forms.CharField(label="Labran nimi")
    description = forms.CharField(label="Kuvaus")
    max_students = forms.IntegerField(label="Oppilasmäärä")
