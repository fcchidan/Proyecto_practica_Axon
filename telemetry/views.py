from rest_framework import viewsets
from .models import SensorReading
from .serializers import SensorReadingSerializer

class SensorReadingViewSet(viewsets.ReadOnlyModelViewSet):
    # Obtenemos todas las lecturas ordenadas de la más reciente a la más antigua, limitadas a las últimas 50
    queryset = SensorReading.objects.all().order_by('-timestamp')[:50]
    serializer_class = SensorReadingSerializer