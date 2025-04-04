from django.urls import path
from .views import consultar_historia_clinica, crear_historia_clinica, verificar_paciente

urlpatterns = [
    path("historia-clinica/<str:cedula>/", consultar_historia_clinica, name="historia_clinica"),
    path('crear-historia-clinica/<str:cedula>/', crear_historia_clinica, name='crear_historia_clinica'),
    path('verificar-paciente/<str:cedula>/', verificar_paciente, name='verificar_paciente'),
]