from django.db import models

class Paciente(models.Model):
    # Datos personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=20, blank=True, null=True) 

    # Identificación y contacto
    cedula = models.CharField(max_length=20, unique=True)  
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    # Información médica
    tipo_sangre = models.CharField(max_length=10, blank=True, null=True) 
    eps = models.CharField(max_length=100, blank=True, null=True)  

    # Contacto de emergencia
    contacto_emergencia_nombre = models.CharField(max_length=100, blank=True, null=True)
    contacto_emergencia_telefono = models.CharField(max_length=15, blank=True, null=True)
    relacion_contacto = models.CharField(max_length=50, blank=True, null=True)  # Texto libre

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"