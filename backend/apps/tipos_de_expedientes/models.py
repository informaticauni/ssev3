import os
from django.db import models
from apps.dependencias.models import Dependencia


class Tipo_de_expediente(models.Model):
    descripcion = models.CharField(null=False, blank=False, max_length=50)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Tipos de Expedientes"

    def __str__(self):
        return str(self.descripcion)


class Tipo_de_expediente_detalle(models.Model):
    tipo_de_expediente_id = models.ForeignKey(Tipo_de_expediente, null=False, blank=False, on_delete=models.CASCADE)
    dependencia_id = models.ForeignKey(Dependencia, null=False, blank=False, on_delete=models.CASCADE)
    orden = models.IntegerField(blank=True, null=False)

    class Meta:
        verbose_name_plural = "Tipos de Expedientes Detalles / Rutas"

    def __str__(self):
        return str(self.tipo_de_expediente_id)+" - "+str(self.dependencia_id)+" - "+str(self.orden)