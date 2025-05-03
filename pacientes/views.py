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
from django.contrib.auth.decorators import login_required

historia_clinica_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max = 2,
    reset_timeout = 60
)

@login_required
def consultar_historia_clinica(request, cedula):
    try:
        verificar_cedula(request, cedula)
        data = get_historia_clinica(cedula)

        if "error" in data:
            raise Http404(data["error"])

        return render(request, "historia_clinica.html", data)

    except Http404:
        raise

    except CircuitBreakerError:
        return render(request, "error_historia_clinica.html", status=503)
    
from django.contrib.auth.decorators import login_required
from monitoring.auth0backend import getRole
from datetime import date
from django.http import HttpResponseForbidden

@login_required
def consultar_historia_clinica(request, cedula):
    try:
        verificar_cedula(request, cedula)
        role = getRole(request)

        if role == "Administrativo":
            paciente = Paciente.objects.filter(cedula=cedula).first()
            if not paciente:
                raise Http404("Paciente no encontrado")

            edad = (date.today() - paciente.fecha_nacimiento).days // 365
            if edad < 18:
                return HttpResponseForbidden("No tiene permisos para consultar historias clínicas de menores de edad.")

        data = get_historia_clinica(cedula)
        if "error" in data:
            raise Http404(data["error"])

        return render(request, "historia_clinica.html", data)

    except Http404:
        raise

    except CircuitBreakerError:
        return render(request, "error_historia_clinica.html", status=503)

@historia_clinica_circuit_breaker
def verificar_cedula(request, cedula):
    if not cedula.isdigit():
        raise Exception("Cédula inválida enviada al sistema")

def verificar_paciente(request, cedula):
    existe = Paciente.objects.filter(cedula=cedula).exists()
    return JsonResponse({'existe': existe})

@csrf_exempt
@login_required
def crear_historia_clinica(request, cedula):
    role = getRole(request)

    if role == "Administrativo":
        return HttpResponseForbidden("No tiene permisos para crear historias clínicas.")
    
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