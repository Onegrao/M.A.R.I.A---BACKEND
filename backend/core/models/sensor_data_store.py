from django.db import models

class DadosMaquina(models.Model):
    vibracao = models.FloatField()
    temperatura = models.FloatField(null = True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dados de {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"