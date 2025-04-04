from django import forms
from .models import SignosVitales

class SignosVitalesForm(forms.ModelForm):
    class Meta:
        model = SignosVitales
        exclude = ['historia_clinica']