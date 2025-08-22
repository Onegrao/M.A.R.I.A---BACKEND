from django.db import models

class DadosMaquina(models.Model):
    machine_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(null = True, blank=True)
    voltage = models.FloatField(null = True, blank=True)
    amperage = models.FloatField(null = True, blank=True)
    pressure = models.FloatField(null = True, blank=True)
    rpm = models.FloatField(null = True, blank=True)
    

    def __str__(self):
        return f"Dados de {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"