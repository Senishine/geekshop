from django.urls import path
from .views import products, upload


app_name = 'mainapp'

urlpatterns = [
    path('', products, name='main'),
    path('upload-data/', upload)
]
