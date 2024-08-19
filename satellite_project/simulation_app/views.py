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
        # last_run = pytz.utc.localize(datetime.datetime.now())
        while True:
            # Note: This commented command uses celery: simulation_satellite_malfunction.delay()
            # -- turning it off for now because celery is having issues from the container atm.
            async for spacecraft in Spacecraft.objects.all():
                # if spacecraft.updated > last_run:
                last_run = pytz.utc.localize(datetime.datetime.now())
                yield _format_message(spacecraft)
            # Using sleep is not my ideal solution.
            # -- My ultimate goal is to use signals from database updates instead.
            await asyncio.sleep(5)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


def _format_message(model):
    data = json.dumps({"name": model.name, "status": model.status, "slug": model.slug}) + "\n\n"
    return f"data: {data}"


def index(request):
    return render(request, 'sse.html')