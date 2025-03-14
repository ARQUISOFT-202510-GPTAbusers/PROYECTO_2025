from ..models import Paciente
from historias_clinicas.models import HistoriaClinica
from signos_vitales.models import SignosVitales

def get_historia_clinica(cedula):
    """Consulta la historia clínica y los signos vitales de un paciente por su cédula."""
    try:
        paciente = Paciente.objects.get(cedula=cedula) 
        historia = HistoriaClinica.objects.get(paciente=paciente)
        signos_vitales = SignosVitales.objects.get(historia_clinica=historia)

        return {
            "paciente": paciente,
            "historia_clinica": historia,
            "signos_vitales": signos_vitales,
        }
    
    except Paciente.DoesNotExist:
        return {"error": "Paciente no encontrado"}
    except HistoriaClinica.DoesNotExist:
        return {"error": "Historia clínica no encontrada"}
    except SignosVitales.DoesNotExist:
        return {"error": "Signos vitales no encontrados"}