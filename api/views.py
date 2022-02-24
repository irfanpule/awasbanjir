import asyncio
import threading
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from perangkat.models import DataSeries, Perangkat
from warga.models import Warga
from awasbanjir import notifications

from api.serializers import DataSeriesSerializer
from api.authentications import DeviceAPIAuthentication


class DataSeriesListView(generics.ListAPIView):
    queryset = DataSeries.objects.all()
    serializer_class = DataSeriesSerializer


class DataSeriesCreateView(generics.CreateAPIView):
    authentication_classes = [DeviceAPIAuthentication]
    serializer_class = DataSeriesSerializer
    perangkat: Perangkat = None

    def post(self, request, *args, **kwargs):
        self.perangkat = get_object_or_404(Perangkat, device_id=request.device_id)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data_series = serializer.save(perangkat=self.perangkat)
        data_series.set_status()
        data_series.refresh_from_db()
        status = get_device_cache(self.request.device_id, data_series.status)
        print(status, data_series.status)
        if status != data_series.status:
            for warga in Warga.objects.all():
                n = notifications.send_telegram_personal(
                    warga.no_hp, f"Awas Banjir!, status {data_series.get_status_display()}")
                asyncio.run(n)


def get_device_cache(device_id, set_status):
    status = cache.get(device_id)
    if not status:
        print("set cache")
        cache.set(device_id, set_status)
        status = set_status
    return status
