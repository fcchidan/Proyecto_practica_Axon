from django.contrib import admin
from .models import SensorReading

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'value', 'unit', 'status', 'timestamp')
    list_filter = ('status', 'sensor_id')
    search_fields = ('sensor_id',)