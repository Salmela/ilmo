"""Module for app logic."""
from django.http import HttpResponse
import os

def save_file(file):
    """
        save file to filesystem
    """
    with open("ilmoweb/static/upload/" + file.name, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def download_file(filename):
    """
        download file from filesystem
    """
    file_path = f'ilmoweb/static/upload/{filename}'
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
