from django.urls import path
from website import views


app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
]
