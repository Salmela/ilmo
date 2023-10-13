"""Module for page rendering."""
import json
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ilmoweb.models import User, Courses, Labs, LabGroups, SignUp
#from ilmoweb.forms import NewLabForm
from ilmoweb.logic import labs, signup, labgroups


def home_page_view(request):
    """
        Homepage view.

    """
    return render(request, "home.html")

@login_required
def created_labs(request):
    """
        View for all created labs.
    """
    if request.user.is_staff is not True:
        return redirect("/open_labs")

    courses = Courses.objects.all()
    return render(request, "created_labs.html", {"courses":courses})

@login_required
def create_lab(request):
    """
        View for creating a new lab.
    """
    if request.method == "GET":
        if request.user.is_staff is not True:
            return redirect("/open_labs")

    if request.method == "POST":
        lab_name = request.POST.get("lab_name")
        description = request.POST.get("description")
        max_students = int(request.POST.get("max_students"))
        course_id = request.POST.get("course_id")

        labs.create_new_lab(lab_name, description, max_students, course_id)

        return created_labs(request)

    course_id = request.GET.get("course_id")

    return render(request, "create_lab.html", {"course_id": course_id})

@login_required
def open_labs(request):
    """
        View for labs that are open
    """
    courses =  Courses.objects.all()
    course_labs =  Labs.objects.all()
    lab_groups =  LabGroups.objects.all()
    signedup = SignUp.objects.all()

    if request.method == "POST":
        if request.user.is_staff:
            return HttpResponseBadRequest('Opettaja ei voi ilmoittautua laboratoriotyöhön.')
        data = json.loads(request.body)
        user_id = data.get('user_id')
        group_id = data.get('group_id')
        user = get_object_or_404(User, pk = user_id)
        group = get_object_or_404(LabGroups, pk = group_id)
        signup.signup(user=user, group=group)

    return render(request, 'open_labs.html', {"courses":courses, "labs":course_labs,
                                              "lab_groups":lab_groups, "signedup":signedup})

@login_required
def confirm(request):
    """
        request for confirming a labgroup
    """
    if request.method == "POST":
        if request.user.is_staff:
            group_id = json.loads(request.body)
            labgroup = LabGroups.objects.get(pk=group_id)
            if labgroup.signed_up_students > 0:
                labgroups.confirm(group_id)
                return HttpResponseRedirect("/open_labs")
        else:
            return HttpResponseBadRequest('Oppilas ei voi vahvistaa laboratoriotyötä.')
    return HttpResponseBadRequest('Ryhmä on tyhjä, joten vahvistaminen epäonnistui.')

@login_required
def delete_lab(request, course_id):
    """
        Delete lab from created_labs view.
    """
    lab = Labs.objects.get(pk=course_id)
    lab.deleted=1
    lab.save()
    courses = Courses.objects.all()

    return render(request, "created_labs.html", {"lab":lab, "courses":courses})

@login_required
def my_labs(request):
    """
        my labs view
    """
    return render(request, "my_labs.html")
