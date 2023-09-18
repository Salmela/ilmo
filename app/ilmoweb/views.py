"""Module for page rendering."""
#from django.http import HttpResponse  #currently unused. Changed to django.shortcuts render.
#from django.template import loader
from django.shortcuts import render
from ilmoweb.models import User


def home_page_view(request):    # pylint: disable=unused-argument
    """
        Homepage template.

    """
    return render(request, 'home.html')

def database_test_view(request):
    """
        Database test template.
    """
    test_data = User.objects.all()    # pylint: disable=no-member
    context = {"users":test_data}
    print(context)

    return render(request, 'database_test.html', context)