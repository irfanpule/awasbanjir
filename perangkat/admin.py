from django.contrib import admin
from .models import Perangkat, DataSeries


class AdminPerangkat(admin.ModelAdmin):
    list_display = ('nama', 'device_id', 'tipe', 'lokasi', 'pemilik')
    search_fields = ('nama', 'device_id')


class AdminDataSeries(admin.ModelAdmin):
    list_display = ('perangkat', 'jarak', 'status')
    search_fields = ('perangkat__nama', 'status')


admin.site.register(Perangkat, AdminPerangkat)
admin.site.register(DataSeries, AdminDataSeries)
