from django.http import HttpResponse
from django.template import loader
from .tasks import simulation_satellite_malfunction
import random
from simulation_app.models import Spacecraft


def main_page(request):
    template = loader.get_template('landing.html')
    simulation_satellite_malfunction.delay()
    return HttpResponse(template.render())
