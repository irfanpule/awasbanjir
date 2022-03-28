from django.urls import path
from website import views


app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('get-point-devices/', views.get_point_devices, name='get_point_device'),
]
