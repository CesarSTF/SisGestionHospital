from django.db import models
from enum import Enum
from abc import ABC, abstractmethod

class EspecialidadMedica(Enum):
    CARDIOLOGIA = 'Cardiologia'
    PEDIATRIA = 'Pediatria'
    DERMATOLOGIA = 'Dermatologia'
    NEUROLOGIA = 'Neurologia'
    NEUMOLOGIA = 'Neumologia'
    UROLOGIA = 'Urologia'

class AbstractPersona(models.Model):
    identificador = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    salud = models.IntegerField(default=100)

    def estado_salud(self):
        return self.salud > 50

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True

class Doctor(AbstractPersona):
    especialidad = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in EspecialidadMedica])

    def dar_resultado(self):
        return "Resultado"

    def __str__(self):
        return self.nombre

class Paciente(AbstractPersona):
    doctor = models.ForeignKey(Doctor, related_name="pacientes", on_delete=models.CASCADE)
    expediente_medico = models.ManyToManyField('ExpedienteMedico', related_name="pacientes")
    cita_medica = models.ManyToManyField('CitaMedica', related_name="pacientes")

    def __str__(self):
        return self.nombre

class Enfermero(AbstractPersona):
    pacientes = models.ManyToManyField(Paciente, related_name="enfermeros")

    def __str__(self):
        return self.nombre

class CitaMedica(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    motivo_cita = models.CharField(max_length=100)
    paciente = models.ForeignKey(Paciente, related_name="citas_medicas", on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name="citas_medicas", on_delete=models.CASCADE)

    def __str__(self):
        return f"Cita de {self.paciente} con {self.doctor} para {self.fecha} a las {self.hora}"

class ExpedienteMedico(models.Model):
    historia_clinica = models.TextField()
    diagnostico_medico = models.TextField()
    contacto_emergencia = models.CharField(max_length=10)
    tratamiento = models.TextField()

    def __str__(self):
        return f"Expediente con diagnóstico {self.diagnostico_medico} y tratamiento {self.tratamiento}"

class GestionCita(ABC):
    @abstractmethod
    def programarCita(self):
        pass

    @abstractmethod
    def generarCita(self):
        pass

    @abstractmethod
    def cancelarCita(self):
        pass

    @abstractmethod
    def reagendarCita(self):
        pass
