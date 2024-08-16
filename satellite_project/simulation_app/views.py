import logging

import datetime
import pytz
from pydantic import json

from .models import Spacecraft
from .tasks import simulation_satellite_malfunction
import asyncio
import json

from django.http import StreamingHttpResponse
from django.shortcuts import render


def landing(request):
    return render(request, 'landing.html')


async def sse_stream(request):
    """
    Sends server-sent events to the client.
    """
    async def event_stream():
        logging.basicConfig(filename='simulation_app.log', level=logging.INFO)
        # Not my ideal solution, ultimate goal is to use signals from database updates
        last_run = pytz.utc.localize(datetime.datetime.now())
        while True:
            simulation_satellite_malfunction.delay()
            async for spacecraft in Spacecraft.objects.all():
                logging.info(spacecraft)
                logging.info(last_run)
                if spacecraft.updated > last_run:
                    last_run = pytz.utc.localize(datetime.datetime.now())
                    yield _format_message(spacecraft)

            await asyncio.sleep(5)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


def _format_message(model):
    data = json.dumps({"name": model.name, "status": model.status}) + "\n\n"
    return f"data: {data}"


def index(request):
    return render(request, 'sse.html')