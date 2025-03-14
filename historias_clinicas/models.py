from django.db import models
from pacientes.models import Paciente

class HistoriaClinica(models.Model):
    # Paciente 
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name="historia_clinica")

    # Antecedentes Médicos
    antecedentes_personales = models.TextField(blank=True, null=True)  
    antecedentes_familiares = models.TextField(blank=True, null=True) 
    alergias = models.TextField(blank=True, null=True)  
    medicamentos_actuales = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"Historia Clínica de {self.paciente.nombre} {self.paciente.apellido}"