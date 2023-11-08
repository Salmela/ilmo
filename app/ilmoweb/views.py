"""Module for page rendering."""
import datetime
import os
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ilmoweb.models import User, Courses, Labs, LabGroups, SignUp, Report
from ilmoweb.logic import labs, signup, labgroups, files

def home_page_view(request):
    """
        Homepage view
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect(created_labs)
        return redirect(open_labs)
    return render(request, "home.html")

@login_required
def created_labs(request):
    """
        View for all created labs
    """
    if request.user.is_staff is not True:
        return redirect("/open_labs")

    courses = Courses.objects.all()
    course_labs = Labs.objects.filter(is_visible=1)
    lab_groups = LabGroups.objects.filter(deleted=0).order_by('date')
    return render(request, "created_labs.html", {"courses":courses, "labs":course_labs,
                                                 "lab_groups":lab_groups})

@login_required
def create_lab(request):
    """
        View for creating a new lab
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

        return redirect(created_labs)
    course_id = request.GET.get("course_id")

    return render(request, "create_lab.html", {"course_id": course_id})

@login_required
def create_group(request):
    """
        View for creating a new labgroup
    """
    if request.method == "GET":
        if request.user.is_staff is not True:
            return redirect("/open_labs")

    if request.method == "POST":
        course_labs = request.POST.getlist("labs[]")
        place = request.POST.get("place")
        date = request.POST.get("date")
        time = request.POST.get("time")
        assistant_id = request.POST.get("assistant")

        for lab in course_labs:
            this_lab = Labs.objects.get(pk=lab)
            assistant = User.objects.get(pk=assistant_id)
            labgroups.create(this_lab, date, time, place, assistant)

        return redirect(created_labs)

    course_id = request.GET.get("course_id")
    course = Courses.objects.get(pk=course_id)
    course_labs = Labs.objects.all()

    assistants = User.objects.filter(is_staff=True)

    return render(request, "create_group.html", {
        "labs":course_labs, "course":course, "assistants":assistants})

@login_required
def open_labs(request):
    """
        View for labs that are open
    """
    courses =  Courses.objects.all()
    course_labs =  Labs.objects.all()
    lab_groups =  LabGroups.objects.all()
    signedup = SignUp.objects.all()
    users_enrollments = signup.get_labgroups(request.user)

    return render(request, "open_labs.html", {"courses":courses, "labs":course_labs,
                                              "lab_groups":lab_groups, "signedup":signedup,
                                              "users_enrollments":users_enrollments})

@login_required
def enroll(request):
    """
        A request for student enrolling in a given lab group
    """
    users_enrollments = signup.get_labgroups(request.user)

    if request.method == "POST":
        max_students = request.POST.get("max_students")
        num_of_students = request.POST.get("students")
        user_id = request.POST.get("user_id")
        group_id = request.POST.get("group_id")
        user = get_object_or_404(User, pk = user_id)
        group = get_object_or_404(LabGroups, pk = group_id)

        if request.user.is_staff:
            messages.warning(request, "Opettaja ei voi ilmoittautua laboratoriotyöhön.")

        else:
            for lab_group in users_enrollments:
                if group_id == lab_group:
                    messages.warning(request, "Olet jo ilmoittautunut ryhmään")

            if num_of_students == max_students:
                messages.warning(request, "Et voi ilmoittautua täynnä olevaan ryhmään")

            try:
                signup.signup(user=user, group=group)
                messages.success(request, "Ilmoittautuminen onnistui!")

            except ValueError:
                messages.warning(request, "Ilmoittautuminen epäonnistui")
    return redirect(open_labs)

@login_required
def confirm(request):
    """
        request for confirming a labgroup
    """
    if request.method == "POST":
        group_id = request.POST.get("lab_group_id")
        labgroup = LabGroups.objects.get(pk=group_id)

        if request.user.is_staff:
            if labgroup.signed_up_students == 0:
                messages.warning(request, "Tyhjää ryhmää ei voida vahvistaa")

            elif labgroup.signed_up_students > 0:
                labgroups.confirm(group_id)
                messages.success(request, "Ryhmä vahvistettu")
        else:
            return redirect(open_labs)
    return redirect(open_labs)

@login_required
def make_lab_visible(request, lab_id):
    """
        Toggle the lab's visibility based on its current state.
    """
    if request.user.is_staff:
        lab = Labs.objects.get(pk=lab_id)
        lab.is_visible = not lab.is_visible
        lab.save()

    return redirect(created_labs)

@login_required
def delete_lab(request, lab_id):
    """
        Delete lab from created_labs view.
    """
    if request.user.is_staff:
        lab = Labs.objects.get(pk=lab_id)
        lab.deleted = 1
        lab.save()

    return redirect(created_labs)

@login_required
def my_labs(request):
    """
        My labs view
    """
    labgroup_id_list = signup.get_labgroups(request.user)
    students_labgroups = LabGroups.objects.filter(pk__in=labgroup_id_list)
    students_reports = Report.objects.filter(student_id=request.user.id)
    lg_ids_with_reports = [report.lab_group_id for report in students_reports]
    ids_without_grade = [report.lab_group_id for report in students_reports if report.grade is None]
    return render(request, "my_labs.html", {"labgroups":students_labgroups,
                                            "reports":students_reports,
                                            "labgroup_ids_with_reports":lg_ids_with_reports,
                                            "labgroup_ids_without_grade":ids_without_grade})

@login_required
def return_report(request):
    """
        Path for returning reports
    """
    if request.method != "POST":
        return redirect("/")

    group_id = request.POST.get("lab_group_id")
    lab_group = LabGroups.objects.get(pk=group_id)
    file = request.FILES["file"]
    filename = os.path.basename(str(file))
    print(filename)
    if not file.name.lower().endswith(('.pdf', '.docx')):
        messages.warning(request, "Tiedoston tulee olla pdf tai docx muodossa")
        return redirect("/my_labs")
    report = Report(student=request.user, lab_group=lab_group, filename=filename, report_status=1)
    report.save()
    messages.success(request, "Tiedosto lähetetty onnistuneesti")
    return redirect("/my_labs")

@login_required
def returned_reports(request):
    """
        Teacher's view of all returned reports.
    """
    if request.user.is_staff is not True:
        return redirect("/my_labs")

    courses = Courses.objects.all()
    course_labs = Labs.objects.all()
    lab_groups = LabGroups.objects.all()
    reports = Report.objects.all()
    users = User.objects.all()
    return render(request, "returned_reports.html", {"courses":courses, "labs":course_labs,
    "lab_groups":lab_groups, "reports":reports, "users":users})

@login_required
def returned_report(request, report_id):
    """
        Changes the assistant of a certain report.
    """
    if request.user.is_staff is not True:
        return redirect("/my_labs")

    if request.method == "POST":
        report = Report.objects.get(pk=report_id)
        assistant_id = int(request.POST.get("assistant"))
        report.graded_by_id = assistant_id
        report.save()

    return redirect("/returned_reports")

@login_required
def evaluate_report(request, report_id):
    """
        Teacher's view for evaluating a certain report.
    """
    if request.user.is_staff is not True:
        return redirect("/my_labs")

    report = Report.objects.get(pk=report_id)
    lab_group = LabGroups.objects.get(pk=report.lab_group_id)
    lab = Labs.objects.get(pk=lab_group.lab_id)
    course = Courses.objects.get(pk=lab.course_id)
    student = User.objects.get(pk=report.student_id)

    if request.method == "POST":
        grade = int(request.POST.get("grade"))
        report.grade = grade
        comments = request.POST.get("comments")
        report.comments = comments
        report.grading_date = datetime.date.today()
        report.graded_by_id = request.user.id
        if grade == 0:
            report.report_status = 2
        else:
            report.report_status = 4
        report.save()

        return redirect(returned_reports)

    return render(request, "evaluate_report.html", {"course":course, "lab":lab,
    "lab_group":lab_group, "report":report, "student":student})

@login_required
def download_report(request, filename):
    """
        Teacher can download reports through this view.
    """
    response = files.download_file(filename)
    return response

@login_required
def delete_labgroup(request, labgroup_id):
    """
        Delete course from created_labs view.
    """
    if request.user.is_staff:
        labgroup = LabGroups.objects.get(pk=labgroup_id)
        labgroup.deleted = 1
        labgroup.save()

    return redirect(created_labs)

@login_required
def labgroup_status(request, labgroup_id):
    """
        Toggle labgroups status based on its current state.
    """
    if request.user.is_staff:
        labgroup = LabGroups.objects.get(pk=labgroup_id)
        if labgroup.status == 0:
            labgroup.status = 1
        else:
            labgroup.status = 0
        labgroup.save()

    return redirect(created_labs)

@login_required
def cancel_enrollment(request, labgroup_id):
    """
        Student can cancel an enrollment to a labgroup through this view.
    """
    if request.method == "POST":
        if request.user.is_staff:
            return HttpResponseBadRequest("Opettaja ei voi peruuttaa ilmoittautumista.")
        user = request.user
        signup.cancel(user, labgroup_id)
        messages.success(request, "Ilmoittautuminen peruutettu")

    return redirect("/open_labs")
