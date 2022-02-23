from django.urls import path
from api import views


app_name = 'api'
urlpatterns = [
    path('data-series/', views.DataSeriesListView.as_view(), name='data_series'),
    path('data-series/create/', views.DataSeriesCreateView.as_view(), name='create_data_series')
]
