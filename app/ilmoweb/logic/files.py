"""Module for app logic."""
import os
from django.http import HttpResponse

def download_file(filename):
    """
        download file from filesystem
    """
    file_path = f'ilmoweb/static/upload/{filename}'
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

def delete_file(file_path):
    """
        delete file from filesystem
    """
    os.remove(file_path)
