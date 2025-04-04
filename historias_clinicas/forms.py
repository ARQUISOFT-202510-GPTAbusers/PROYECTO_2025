from django import forms
from .models import HistoriaClinica

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        exclude = ['paciente']