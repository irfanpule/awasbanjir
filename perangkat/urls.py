from django.urls import path
from perangkat import views

app_name = 'perangkat'
urlpatterns = [
    path('list/', views.PerangkatListView.as_view(), name='list'),
    path('create/', views.PerangkatCrateView.as_view(), name='create'),
    path('update/<int:pk>', views.PerangkatUpdateView.as_view(), name='update'),
    path('monitor/<int:pk>', views.PantauView.as_view(), name='monitor'),
    path('get-data-series/<str:device_id>', views.GetDataSeriesView.as_view(), name='get_data_series'),
    path('get-last-data/<str:device_id>', views.GetLastDataView.as_view(), name='get_last_data'),
    path('monitor/list/', views.PantautListView.as_view(), name='monitor_list'),
    path('history/<int:pk>', views.RiwayatView.as_view(), name='history'),
    path('history/get-data-series/<str:device_id>', views.GetDataSeriesHistoryView.as_view(),
         name='get_data_series_history'),
]
