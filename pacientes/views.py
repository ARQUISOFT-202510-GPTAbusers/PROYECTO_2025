from django.shortcuts import render

from django.shortcuts import render
from django.http import Http404
from logic.logic_pacientes import get_historia_clinica

def consultar_historia_clinica(request, cedula):
    data = get_historia_clinica(cedula)

    if "error" in data:
        raise Http404(data["error"]) 

    return render(request, "historia_clinica.html", data)