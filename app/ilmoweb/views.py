"""Module for page rendering."""
import json
from django.http import HttpResponseRedirect, HttpResponseBadRequest
#from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from ilmoweb.models import User, Courses, Labs, LabGroups, SignUp
from ilmoweb.forms import NewLabForm
from ilmoweb.logic import labs, signup, labgroups


def home_page_view(request):
    """
        Homepage view.

    """
    return render(request, "home.html")

def created_labs(request):
    """
        View for all created labs.
    """
    if request.user.is_staff is not True:
        return redirect("/open_labs")

    courses = Courses.objects.all()
    course_labs = Labs.objects.all()
    lab_groups = LabGroups.objects.all()
    return render(request, "created_labs.html", {"courses":courses, "labs":course_labs,
                                                 "lab_groups":lab_groups})

def create_lab(request):
    """
        View for creating a new lab.
    """
    if request.method == "GET":
        if request.user.is_staff is not True:
            return redirect("/open_labs")

    if request.method == "POST":
        form = NewLabForm(request.POST)
        course_id = request.POST.get("course_id")

        if form.is_valid():
            content = form.cleaned_data

        labs.create_new_lab(content, course_id)

        return redirect("/created_labs")
    course_id = request.GET.get("course_id")
    form = NewLabForm

    return render(request, "create_lab.html", {"form": form, "course_id": course_id})

def create_group(request):
    """
        View for creating a new labgroup
    """
    if request.method == "GET":
        if request.user.is_staff is not True:
            return redirect("/open_labs")

    if request.method == "POST":
        course_labs = request.POST.getlist('labs[]')
        place = request.POST.get("place")
        date = request.POST.get("date")
        time = request.POST.get("time")

        for lab in course_labs:
            this_lab = Labs.objects.get(pk=lab)
            labgroups.create(this_lab, date, time, place)

        return created_labs(request)

    course_id = request.GET.get("course_id")
    course = Courses.objects.get(pk=course_id)
    course_labs = Labs.objects.all()

    return render(request, "create_group.html", {"labs":course_labs, "course":course})

def open_labs(request):
    """
        View for labs that are open
    """
    courses =  Courses.objects.all()
    course_labs =  Labs.objects.all()
    lab_groups =  LabGroups.objects.all()
    signedup = SignUp.objects.all()

    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get('user_id')
        group_id = data.get('group_id')
        user = get_object_or_404(User, pk = user_id)
        group = get_object_or_404(LabGroups, pk = group_id)
        signup.signup(user=user, group=group)

    return render(request, 'open_labs.html', {"courses":courses, "labs":course_labs,
                                              "lab_groups":lab_groups, "signedup":signedup})

def confirm(request):
    """
        request for confirming a labgroup
    """
    if request.method == "POST":
        group_id = json.loads(request.body)
        labgroup = LabGroups.objects.get(pk=group_id)
        if labgroup.signed_up_students > 0:
            labgroups.confirm(group_id)
            return HttpResponseRedirect("/open_labs")
    return HttpResponseBadRequest('Ryhmä on tyhjä, joten vahvistaminen epäonnistui.')

def delete_lab(request, course_id):
    """
        Delete lab from created_labs view.
    """
    lab = Labs.objects.get(pk=course_id)
    lab.deleted=1
    lab.save()
    courses = Courses.objects.all()

    return render(request, "created_labs.html", {"lab":lab, "courses":courses})

def my_labs(request):
    """
        my labs view
    """
    return render(request, "my_labs.html")
