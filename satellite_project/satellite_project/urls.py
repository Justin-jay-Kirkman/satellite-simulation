from django.contrib import admin
from django.urls import path
from simulation_app.api import api
from simulation_app.views import main_page

urlpatterns = [
    path('', main_page, name='main_page'),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
