"""Module for page rendering."""
#from django.http import HttpResponse  #currently unused. Changed to django.shortcuts render.
#from django.template import loader
import json
from django.shortcuts import render, redirect, get_object_or_404
from ilmoweb.models import User, Courses, Labs, LabGroups, SignUp
from ilmoweb.forms import NewLabForm
from ilmoweb.logic import labs, signup


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
    return render(request, "created_labs.html", {"courses":courses})

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

        return created_labs(request)

    course_id = request.GET.get("course_id")
    form = NewLabForm

    return render(request, "create_lab.html", {"form": form, "course_id": course_id})

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
