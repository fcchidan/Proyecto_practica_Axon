import os
import django
import random
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Configurar el entorno de Django para poder usar modelos y canales fuera del servidor web
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scada_project.settings')
django.setup()

from telemetry.models import SensorReading

channel_layer = get_channel_layer()

print("==========================================")
print("  Iniciando Simulador SCADA / PLC...")
print("  Presiona Ctrl+C para detener el servicio.")
print("==========================================")

# Definimos sensores simulados de una planta industrial
sensors = [
    {"id": "REACTOR_TEMP", "unit": "°C", "min": 60, "max": 120},
    {"id": "PRESION_ESTANQUE", "unit": "PSI", "min": 10, "max": 50},
    {"id": "CAUDAL_BOMBA", "unit": "L/s", "min": 5, "max": 25},
]

while True:
    try:
        # Seleccionar un sensor al azar y generar un valor numérico aleatorio
        sensor = random.choice(sensors)
        val = round(random.uniform(sensor["min"], sensor["max"]), 2)
        
        # Evaluar el estado según el valor (si supera el 85% del máximo, pasa a WARNING)
        status = "OK" if val < (sensor["max"] * 0.85) else "WARNING"

        # 1. Guardar la lectura en la Base de Datos (Persistencia histórica)
        reading = SensorReading.objects.create(
            sensor_id=sensor["id"],
            value=val,
            unit=sensor["unit"],
            status=status
        )

        # 2. Preparar el paquete de datos para enviarlo en tiempo real por WebSocket
        data = {
            "sensor_id": reading.sensor_id,
            "value": reading.value,
            "unit": reading.unit,
            "status": reading.status,
            "timestamp": reading.timestamp.isoformat()
        }
        
        # Enviar el mensaje al grupo 'scada_live' a través del Channel Layer
        async_to_sync(channel_layer.group_send)(
            "scada_live",
            {
                "type": "send_sensor_update",
                "data": data
            }
        )
        
        print(f"[SCADA] Dato enviado y guardado -> {sensor['id']}: {val} {sensor['unit']} [{status}]")
        
        # Esperar 2 segundos antes de la siguiente lectura
        time.sleep(2)

    except KeyboardInterrupt:
        print("\nSimulador detenido por el usuario.")
        break