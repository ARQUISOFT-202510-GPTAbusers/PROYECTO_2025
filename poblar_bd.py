import os
import django
import random
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitoring.settings") 
django.setup()

from pacientes.models import Paciente
from historias_clinicas.models import HistoriaClinica
from signos_vitales.models import SignosVitales

def poblar_base_datos(n=10000):
    fake = Faker()
    
    for _ in range(n):
        paciente = Paciente(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            fecha_nacimiento=fake.date_of_birth(minimum_age=5, maximum_age=90),
            genero=random.choice(["Masculino", "Femenino", "Otro"]),
            cedula=fake.unique.random_number(digits=10),
            correo=fake.unique.email(),
            telefono=fake.numerify(text='###########'),
            direccion=fake.address(),
            tipo_sangre=random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
            eps=fake.company(),
            contacto_emergencia_nombre=fake.name(),
            contacto_emergencia_telefono=fake.numerify(text='###########'),
            relacion_contacto=random.choice(["Padre", "Madre", "Hermano", "Pareja", "Amigo", "Otro"])
        )
        paciente.save()

        historia = HistoriaClinica(
            paciente=paciente,
            antecedentes_personales=fake.text(),
            antecedentes_familiares=fake.text(),
            alergias=fake.text(),
            medicamentos_actuales=fake.text()
        )
        historia.save()

        signos = SignosVitales(
            historia_clinica=historia,
            fecha_medicion=fake.date_time_this_year(),
            presion_arterial=f"{random.randint(90, 140)}/{random.randint(60, 90)}",
            frecuencia_cardiaca=random.randint(60, 100),
            frecuencia_respiratoria=random.randint(12, 20),
            temperatura=round(random.uniform(36.0, 39.0), 1),
            saturacion_oxigeno=random.randint(95, 100)
        )
        signos.save()

if __name__ == "__main__":
    poblar_base_datos()