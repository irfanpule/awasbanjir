from django.contrib import admin
from .models import Perangkat, DataSeries
from mapbox_location_field.admin import MapAdmin


class AdminPerangkat(MapAdmin):
    list_display = ('nama', 'device_id', 'tipe', 'pemilik')
    search_fields = ('nama', 'device_id')


class AdminDataSeries(admin.ModelAdmin):
    list_display = ('perangkat', 'jarak', 'status')
    search_fields = ('perangkat__nama', 'status')


admin.site.register(Perangkat, AdminPerangkat)
admin.site.register(DataSeries, AdminDataSeries)
