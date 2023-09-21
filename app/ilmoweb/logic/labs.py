"""Module for app logic."""
from ilmoweb.models import Labs, Courses

def create_new_lab(content, course_id):
    """
        Saves a new lab to database.

    """
    course = Courses.objects.get(pk=course_id)
    lab = Labs(course=course, name=content["name"], description=content["description"], max_students=content["max_students"], is_visible=False)
    lab.save()