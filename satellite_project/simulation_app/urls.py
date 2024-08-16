from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('simulation/', views.index, name='index'),
    path('stream/', views.sse_stream, name='sse_stream'),
]