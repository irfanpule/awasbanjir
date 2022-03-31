from django.urls import path
from perangkat import views

app_name = 'perangkat'
urlpatterns = [
    path('list/', views.PerangkatListView.as_view(), name='list'),
    path('create/', views.PerangkatCrateView.as_view(), name='create'),
    path('update/<int:pk>', views.PerangkatUpdateView.as_view(), name='update'),
    path('monitor/<int:pk>', views.PantauView.as_view(), name='monitor'),
    path('get-data-series/<str:device_id>', views.get_data_series, name='get_data_series'),
    path('get-last-data/<str:device_id>', views.get_last_data, name='get_last_data'),
    path('monitor/list/', views.PantautListView.as_view(), name='monitor_list'),
]
