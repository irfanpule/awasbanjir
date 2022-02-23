from django.urls import path
from api import views

urlpatterns = [
    path('data-series/', views.DataSeriesListView.as_view(), name='data_series')
]
