from django.http import HttpResponse
from django.template import loader


def main_page(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())
