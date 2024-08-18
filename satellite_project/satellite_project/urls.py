from django.contrib import admin
from django.urls import path, include
from simulation_app.api import api


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', include('simulation_app.urls')),
    path('', include('vue.urls')),
]
