from rest_framework import generics
from alat.models import DataSeries
from api.serializers import DataSeriesSerializer


class DataSeriesListView(generics.ListAPIView):
    queryset = DataSeries.objects.all()
    serializer_class = DataSeriesSerializer
