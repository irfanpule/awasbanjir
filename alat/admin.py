from django.contrib import admin
from .models import Alat, DataSeries


class AdminAlat(admin.ModelAdmin):
    list_display = ('nama', 'unique_id', 'tipe', 'lokasi')
    search_fields = ('nama', 'unique_id')


class AdminDataSeries(admin.ModelAdmin):
    list_display = ('alat', 'jarak', 'status')
    search_fields = ('alat__nama', 'status')


admin.site.register(Alat, AdminAlat)
admin.site.register(DataSeries, AdminDataSeries)
