from django.urls import path
from perangkat import views

app_name = 'perangkat'
urlpatterns = [
    path('list/', views.PerangkatListView.as_view(), name='list'),
    path('create/', views.PerangkatCrateView.as_view(), name='create'),
    path('update/<int:pk>', views.PerangkatUpdateView.as_view(), name='update'),
]
