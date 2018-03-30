from django.urls import path

from . import views

app_name = 'recognition'
urlpatterns = [
    path('', views.home),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('process/', views.process, name='process'),
    path('results/', views.results, name='results'),
]