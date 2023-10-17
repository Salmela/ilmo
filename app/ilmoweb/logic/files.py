"""Module for app logic."""

def save_file(file):
    """
        save file to filesystem
    """
    with open("ilmoweb/static/upload/" + file.name, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
