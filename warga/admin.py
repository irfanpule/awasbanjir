from django.contrib import admin
from .models import Warga


class AdminWarga(admin.ModelAdmin):
    list_display = ('user', 'nama_desa', 'no_hp')
    search_fields = ('nama', 'device_id')


admin.site.register(Warga, AdminWarga)
