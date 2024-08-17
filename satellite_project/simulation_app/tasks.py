import logging
import random
from simulation_app.models import Spacecraft
from celery import shared_task


@shared_task(bind=True)
def simulation_satellite_malfunction(self):
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    try:
        spacecrafts = list(Spacecraft.objects.all())
        if len(spacecrafts) != 0:
            random_item = random.choice(spacecrafts)
            random_status = random.choice(["MALFUNCTIONING", "NOMINAL"])
            random_item.status = random_status
            random_item.save()
            return "Malfunction was successfully simulated for " + random_item.name
    except Exception as e:
        logging.error(e)
        return "Error in simulation_satellite_malfunction"
    return "No items to update " + str(len(spacecrafts))

