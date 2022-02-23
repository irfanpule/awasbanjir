from rest_framework import generics
from django.shortcuts import get_object_or_404

from perangkat.models import DataSeries, Perangkat
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
        print(self.perangkat)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data_series = serializer.save(perangkat=self.perangkat)
        data_series.set_status()
