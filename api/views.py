from rest_framework import generics
from django.shortcuts import get_object_or_404

from alat.models import DataSeries, Alat
from api.serializers import DataSeriesSerializer
from api.authentications import DeviceAPIAuthentication


class DataSeriesListView(generics.ListAPIView):
    queryset = DataSeries.objects.all()
    serializer_class = DataSeriesSerializer


class DataSeriesCreateView(generics.CreateAPIView):
    authentication_classes = [DeviceAPIAuthentication]
    serializer_class = DataSeriesSerializer
    alat: Alat = None

    def post(self, request, *args, **kwargs):
        self.alat = get_object_or_404(Alat, unique_id=request.device_id)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data_series = serializer.save(alat=self.alat)
        data_series.set_status()
