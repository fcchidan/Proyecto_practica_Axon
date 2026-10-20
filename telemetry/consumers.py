import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ScadaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "scada_live"
        
        # Unirse al grupo de difusión general del SCADA
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo al desconectarse
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Este método recibe los eventos enviados desde el script de Python o backend
    async def send_sensor_update(self, event):
        data = event['data']
        # Enviar los datos en formato JSON al navegador (React)
        await self.send(text_data=json.dumps(data))