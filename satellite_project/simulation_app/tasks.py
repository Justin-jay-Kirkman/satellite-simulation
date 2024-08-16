import random
from simulation_app.models import Spacecraft
from celery import shared_task

@shared_task(bind=True)
def simulation_satellite_malfunction(self):
    spacecrafts = list(Spacecraft.objects.all())
    if len(spacecrafts) != 0:
        random_item = random.choice(spacecrafts)
        random_item.status = "MALFUNCTIONING"
        random_item.save()
        return "Malfunction was successfully simulated"
    return "No items to update"
