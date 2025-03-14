from django.db import models
from historias_clinicas.models import HistoriaClinica

class SignosVitales(models.Model):
    # Historia clínica
    historia_clinica = models.OneToOneField(HistoriaClinica, on_delete=models.CASCADE, related_name="signos_vitales")

    fecha_medicion = models.DateTimeField(auto_now_add=True) 
    presion_arterial = models.CharField(max_length=10, blank=True, null=True) 
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True)  
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True) 
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True) 
    saturacion_oxigeno = models.IntegerField(blank=True, null=True)  

    def __str__(self):
        return f"Signos vitales de {self.historia_clinica.paciente} - {self.fecha_medicion.strftime('%Y-%m-%d')}"