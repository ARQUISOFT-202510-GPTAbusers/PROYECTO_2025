from django.db import models
from historias_clinicas.models import HistoriaClinica

class SignosVitales(models.Model):
    # Historia clínica
    historia_clinica = models.OneToOneField(HistoriaClinica, on_delete=models.CASCADE, related_name="signos_vitales")

    # Signos vitales
    fecha_medicion = models.DateTimeField(auto_now_add=True) 
    presion_arterial = models.CharField(max_length=10) 
    frecuencia_cardiaca = models.IntegerField()  
    frecuencia_respiratoria = models.IntegerField() 
    temperatura = models.DecimalField(max_digits=4, decimal_places=1) 
    saturacion_oxigeno = models.IntegerField()  

    def __str__(self):
        return f"Signos vitales de {self.historia_clinica.paciente} - {self.fecha_medicion.strftime('%Y-%m-%d')}"