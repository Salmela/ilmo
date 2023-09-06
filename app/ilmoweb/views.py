"""Module for page rendering."""
from django.http import HttpResponse
from django.template import loader


def home_page_view(request):    # pylint: disable=unused-argument
    """
        Homepage template.
    
    """
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
