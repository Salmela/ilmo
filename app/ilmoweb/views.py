"""Module for page rendering."""
import datetime
import urllib.request
import json
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Max, F, Subquery, OuterRef
from authlib.integrations.django_client import OAuth
from authlib.oidc.core import CodeIDToken
from authlib.jose import jwt
from ilmoweb.models import User, Courses, Labs, LabGroups, SignUp, Report
from ilmoweb.logic import labs, signup, labgroups, files, check_previous_reports


CONF_URL = 'https://login-test.it.helsinki.fi/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='ilmoweb',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid profile'
    }
)

claims_data = {
        "id_token": {
            "hyPersonStudentId": None,

        },
        "userinfo": {
            "email": None,
            "given_name": None,
            "family_name": None,
            "uid": None
        }
    }

claims = json.dumps(claims_data)

with urllib.request.urlopen("https://login-test.it.helsinki.fi/idp/profile/oidc/keyset") as url:
    keys = json.load(url)

def login(request):
    """
        University login
    """
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.ilmoweb.authorize_redirect(request, redirect_uri, claims=claims)

def auth(request):
    """
        University authentication
    """
    token = oauth.ilmoweb.authorize_access_token(request)

    userinfo = oauth.ilmoweb.userinfo(token=token)
    userdata = jwt.decode(token['id_token'], keys, claims_cls=CodeIDToken)
    userdata.validate()

    user = django_authenticate(userinfo=userinfo)
    if user is not None:
        django_login(request, user)

    return redirect(home_page_view)

def home_page_view(request):
    """
        Homepage view
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect(created_labs)
        return redirect(open_labs)
    return render(request, "home.html")

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        assistant_id = request.POST.get("assistant")

        for lab in course_labs:
            this_lab = Labs.objects.get(pk=lab)
            assistant = User.objects.get(pk=assistant_id)
            labgroups.create(this_lab, date, start_time, end_time, place, assistant)

        return redirect(created_labs)

    course_id = request.GET.get("course_id")
    course = Courses.objects.get(pk=course_id)
    course_labs = Labs.objects.all()

    assistants = User.objects.filter(is_staff=True)

    return render(request, "create_group.html", {
        "labs":course_labs, "course":course, "assistants":assistants})

@login_required(login_url='login')
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


@login_required(login_url='login')

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

@login_required(login_url='login')
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

@login_required(login_url='login')
def make_lab_visible(request, lab_id):
    """
        Toggle the lab's visibility based on its current state.
    """
    if request.user.is_staff:
        lab = Labs.objects.get(pk=lab_id)
        lab.is_visible = not lab.is_visible
        lab.save()

    return redirect(created_labs)

@login_required(login_url='login')
def delete_lab(request, lab_id):
    """
        Delete lab from created_labs view.
    """
    if request.user.is_staff:
        lab = Labs.objects.get(pk=lab_id)
        lab.deleted = 1
        lab.save()

    return redirect(created_labs)

@login_required(login_url='login')
def my_labs(request):
    """
        My labs view
    """
    labgroup_id_list = signup.get_labgroups(request.user)
    students_labgroups = LabGroups.objects.filter(pk__in=labgroup_id_list)
    students_reports = Report.objects.filter(student_id=request.user)
    lg_ids_with_reports = [report.lab_group_id for report in students_reports]
    ids_without_grade = [report.lab_group_id for report in students_reports if report.grade is None]

    # Filter the report with the highest status per labgroup
    reports = Report.objects.filter(student=request.user)
    subquery = reports.filter(lab_group=OuterRef('lab_group')).values('lab_group').annotate(
        max_report_status=Max('report_status')).values('max_report_status')
    reports = reports.annotate(max_report_status=Subquery(subquery))
    filtered_reports = reports.filter(report_status=F('max_report_status'))

    return render(request, "my_labs.html", {"labgroups":students_labgroups,
                                            "reports":students_reports,
                                            "filtered_reports":filtered_reports,
                                            "labgroup_ids_with_reports":lg_ids_with_reports,
                                            "labgroup_ids_without_grade":ids_without_grade})

@login_required(login_url='login')
def return_report(request):
    """
        Path for returning reports
    """
    if request.method != "POST":
        return redirect("/")

    group_id = request.POST.get("lab_group_id")
    lab_group = LabGroups.objects.get(pk=group_id)
    file = request.FILES["file"]
    student = request.user

    if not file.name.lower().endswith(('.pdf')):
        messages.warning(request, "Tiedoston tulee olla pdf-muodossa")
        return redirect("/my_labs")

    prev_1 = Report.objects.filter(student=student, lab_group=lab_group, report_status=1)
    prev_2 = Report.objects.filter(student=student, lab_group=lab_group, report_status=2)
    prev_3 = Report.objects.filter(student=student, lab_group=lab_group, report_status=3)
    prev_4 = Report.objects.filter(student=student, lab_group=lab_group, report_status=4)

    check_previous_reports.check_and_replace(request,
                                            prev_1,
                                            prev_2,
                                            prev_3,
                                            prev_4,
                                            student,
                                            lab_group,
                                            file)

    return redirect("/my_labs")

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def download_report(request, filename):
    """
        Teacher can download reports through this view.
    """
    response = files.download_file(filename)
    return response

@login_required(login_url='login')
def delete_labgroup(request, labgroup_id):
    """
        Delete course from created_labs view.
    """
    if request.user.is_staff:
        labgroup = LabGroups.objects.get(pk=labgroup_id)
        labgroup.deleted = 1
        labgroup.save()

    return redirect(created_labs)


@login_required(login_url='login')
def labgroup_status(request, labgroup_id):
    """
        Toggle labgroups status based on its current state.
    """
    if request.user.is_staff:
        labgroup = LabGroups.objects.get(pk=labgroup_id)
        if labgroup.status in (0, 3):
            labgroup.status = 1
        else:
            labgroup.status = 3
            labgroups.email(labgroup, 'cancel')
        labgroup.save()

    return redirect(created_labs)

@login_required(login_url='login')
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

@login_required
def update_group(request, labgroup_id):
    """
        View for updating a new labgroup
    """
    if request.method == "GET":
        if request.user.is_staff is not True:
            return redirect("/open_labs")

    if request.method == "POST":
        labgroup = LabGroups.objects.get(pk=labgroup_id)
        course_labs = request.POST.getlist("labs[]")
        place = request.POST.get("place")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        assistant_id = request.POST.get("assistant")
        assistant = User.objects.get(pk=assistant_id)
        if not date:
            date=labgroup.date
        labgroups.update(date, start_time, end_time, place, assistant, labgroup_id)

        return redirect(created_labs)

    course_id = request.GET.get("course_id")
    course = Courses.objects.get(pk=course_id)
    course_labs = Labs.objects.all()
    labgroup = LabGroups.objects.get(pk=labgroup_id)

    assistants = User.objects.filter(is_staff=True)

    return render(request, "update_group.html", {
        "labs":course_labs, "course":course, "assistants":assistants, "lab_group":labgroup })
