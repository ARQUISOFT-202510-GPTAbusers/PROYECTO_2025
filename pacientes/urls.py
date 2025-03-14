from django.urls import path
from .views import consultar_historia_clinica

urlpatterns = [
    path("historia-clinica/<str:cedula>/", consultar_historia_clinica, name="historia_clinica"),
]