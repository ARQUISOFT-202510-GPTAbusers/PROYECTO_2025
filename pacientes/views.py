from django.shortcuts import render
from django.http import Http404
from .logic.logic_pacientes import get_historia_clinica
from .models import Paciente
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from historias_clinicas.forms import HistoriaClinicaForm
from pacientes.forms import PacienteForm
from signos_vitales.forms import SignosVitalesForm
from django.views.decorators.csrf import csrf_exempt
import pybreaker
from pybreaker import CircuitBreakerError

historia_clinica_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max = 1,
    reset_timeout = 60
)

def consultar_historia_clinica(request, cedula):
    try:
        data = get_historia_clinica(cedula)

        if "error" in data:
            raise Http404(data["error"])

        return _consultar_historia_clinica_con_breaker(request, data)

    except Http404:
        raise

    except CircuitBreakerError:
        return render(request, "error_historia_clinica.html", status=503)

@historia_clinica_circuit_breaker
def _consultar_historia_clinica_con_breaker(request, data):
    return render(request, "historia_clinica.html", data)

def verificar_paciente(request, cedula):
    existe = Paciente.objects.filter(cedula=cedula).exists()
    return JsonResponse({'existe': existe})

@csrf_exempt
def crear_historia_clinica(request, cedula):
    if Paciente.objects.filter(cedula=cedula).exists():
        return HttpResponseBadRequest("Ya existe un paciente con esta cédula.")

    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST)
        historia_form = HistoriaClinicaForm(request.POST)
        signos_form = SignosVitalesForm(request.POST)

        if paciente_form.is_valid() and historia_form.is_valid() and signos_form.is_valid():
            paciente = paciente_form.save(commit=False)
            paciente.cedula = cedula
            paciente.save()

            historia = historia_form.save(commit=False)
            historia.paciente = paciente
            historia.save()

            signos = signos_form.save(commit=False)
            signos.historia_clinica = historia
            signos.save()

            return consultar_historia_clinica(request, cedula)
        else:
            return render(request, 'crear_historia_clinica.html', {
                'paciente_form': paciente_form,
                'historia_form': historia_form,
                'signos_form': signos_form,
                'cedula': cedula,
                'errores': True
            })
    
    paciente_form = PacienteForm(initial={'cedula': cedula})
    historia_form = HistoriaClinicaForm()
    signos_form = SignosVitalesForm()

    return render(request, 'crear_historia_clinica.html', {
        'paciente_form': paciente_form,
        'historia_form': historia_form,
        'signos_form': signos_form,
        'cedula': cedula
    })