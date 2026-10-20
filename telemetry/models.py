from django.db import models

class SensorReading(models.Model):
    sensor_id = models.CharField(max_length=50) # Ej: "REACTOR_TEMP", "VALVULA_01"
    value = models.FloatField()                  # Ej: 85.5
    unit = models.CharField(max_length=20)       # Ej: "°C", "PSI", "L/s"
    status = models.CharField(max_length=20, default="OK") # "OK", "WARNING", "ERROR"
    timestamp = models.DateTimeField(auto_now_add=True)    # Fecha y hora automática

    def __str__(self):
        return f"{self.sensor_id}: {self.value} {self.unit} [{self.status}]"