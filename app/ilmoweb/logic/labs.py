"""Module for app logic."""
from ilmoweb.models import Labs, Courses

def create_new_lab(lab_name, description, max_students, course_id, id_=None):
    """
        Saves a new lab to database.

    """
    course = Courses.objects.get(pk=course_id)

    if max_students <= 0:
        max_students = 1

    if id_ is None:
        lab = Labs(course=course, name=lab_name,
               description=description, max_students=max_students, is_visible=False)
    else:
        lab = Labs(id=id_+1, course=course, name=lab_name,
               description=description, max_students=max_students, is_visible=False)
    lab.save()
