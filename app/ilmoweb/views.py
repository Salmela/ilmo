"""Module for page rendering."""
import datetime
import urllib.request
import json
import environ
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from authlib.integrations.django_client import OAuth
from authlib.oidc.core import CodeIDToken
from authlib.jose import jwt
from ilmoweb.models import User, Courses, Labs, LabGroups, SignUp, Report
from ilmoweb.logic import labs, signup, labgroups, files
from ilmoweb.logic import check_previous_reports, users_info, filter_reports
env = environ.Env()
environ.Env.read_env()

if env("UNI_LOGIN") == 'True':
    CONF_URL = "https://login.helsinki.fi/.well-known/openid-configuration"
else:
    CONF_URL = "https://login-test.it.helsinki.fi/.well-known/openid-configuration"
oauth = OAuth()
oauth.register(
    name="ilmoweb",
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid profile"
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

if env("UNI_LOGIN") == 'True':
    KEYSET = "https://login.helsinki.fi/idp/profile/oidc/keyset"
else:
    KEYSET = "https://login-test.it.helsinki.fi/idp/profile/oidc/keyset"

with urllib.request.urlopen(KEYSET) as url:
    keys = json.load(url)

def login(request):
    """
        University login
    """
    redirect_uri = request.build_absolute_uri(reverse("auth"))
    return oauth.ilmoweb.authorize_redirect(request, redirect_uri, claims=claims)

def auth(request):
    """
        University authentication
    """
    token = oauth.ilmoweb.authorize_access_token(request)

    userinfo = oauth.ilmoweb.userinfo(token=token)
    userdata = jwt.decode(token["id_token"], keys, claims_cls=CodeIDToken)
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

@login_required(login_url="login")
def created_labs(request):
    """
        View for all created labs
    """
    if request.user.is_staff is not True:
        return redirect("/open_labs")

    courses = Courses.objects.all()
    course_labs = Labs.objects.filter(is_visible=1)
    groups = LabGroups.objects.filter(deleted=0).order_by('date')

    lab_groups = LabGroups.objects.select_related('lab__course', 'assistant').filter(deleted=False)

    dates_times = set()
    groups_by_date_time = []

    for lab_group in lab_groups:
        date_time_key = (lab_group.date, lab_group.start_time, lab_group.end_time, lab_group.place)

        if date_time_key not in dates_times:
            dates_times.add(date_time_key)

            dict_entry = {
                'course': lab_group.lab.course,
                'date': lab_group.date,
                'start_time': lab_group.start_time,
                'end_time': lab_group.end_time,
                'place': lab_group.place,
                'labs': Labs.objects.filter(course=lab_group.lab.course, is_visible=1),
                'groups': [group for group in lab_groups if
                           (group.date, group.start_time, group.end_time,
                            group.place) == date_time_key],
                'signup_sum':sum(([group.signed_up_students for group in lab_groups if
                           (group.date, group.start_time, group.end_time,
                            group.place) == date_time_key]), 0)
            }

            groups_by_date_time.append(dict_entry)

    return render(request, "created_labs.html", {"courses":courses, "labs":course_labs,
                                                 "lab_groups":groups,
                                                 'groups_by_date':groups_by_date_time})

@login_required(login_url="login")
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

@login_required(login_url="login")
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

@login_required(login_url="login")
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


@login_required(login_url="login")
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

@login_required(login_url="login")
def confirm(request):
    """
        request for confirming a labgroup
    """
    if request.method == "POST":
        lab_group_ids = request.POST.getlist("lab_groups")
        lab_groups = [LabGroups.objects.get(id=int(group_id)) for group_id in lab_group_ids]


        if request.user.is_staff:
            signed_up = 0
            for labgroup in lab_groups:
                signed_up += labgroup.signed_up_students

            if signed_up == 0:
                messages.warning(request, "Tyhjää ryhmää ei voida vahvistaa")

            elif signed_up> 0:
                for labgroup in lab_groups:
                    labgroups.confirm(labgroup.id)

                messages.success(request, "Ryhmä vahvistettu")
        else:
            return redirect(created_labs)
    return redirect(created_labs)

@login_required(login_url="login")
def make_lab_visible(request, lab_id):
    """
        Toggle the lab's visibility based on its current state.
    """
    if request.user.is_staff:
        lab = Labs.objects.get(pk=lab_id)
        lab.is_visible = not lab.is_visible
        lab.save()

    return redirect(created_labs)


@login_required(login_url="login")
def delete_lab(request, lab_id):
    """
        Delete lab from created_labs view.
    """
    if request.user.is_staff:
        lab = Labs.objects.get(pk=lab_id)
        lab.deleted = 1
        lab.save()

    return redirect(created_labs)


@login_required(login_url="login")
def labgroup_status(request):
    """
        Toggle labgroups status based on its current state.
    """
    if request.method == "POST":
        lab_group_ids = request.POST.getlist("lab_groups")
        lab_groups = [LabGroups.objects.get(id=int(group_id)) for group_id in lab_group_ids]

        if request.user.is_staff:
            for labgroup in lab_groups:
                if labgroup.status in(0, 3):
                    labgroup.status = 1
                else:
                    labgroup.status = 3
                    labgroups.email(labgroup, "cancel")
                labgroup.save()
        return redirect(created_labs)

    return redirect(created_labs)

@login_required(login_url="login")
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
    filtered_reports = filter_reports.filter_report(request.user)

    return render(request, "my_labs.html", {"labgroups":students_labgroups,
                                            "reports":students_reports,
                                            "filtered_reports":filtered_reports,
                                            "labgroup_ids_with_reports":lg_ids_with_reports,
                                            "labgroup_ids_without_grade":ids_without_grade})

@login_required(login_url="login")
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

    if not file.name.lower().endswith((".pdf")):
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

@login_required(login_url="login")
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

@login_required(login_url="login")
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

@login_required(login_url="login")
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
        if "file" in request.FILES:
            comment_file = request.FILES["file"]
            report.comment_file = comment_file
            report.comment_file_name = comment_file.name
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

@login_required(login_url="login")
def download_report(request, filename):
    """
        Teacher can download reports through this view.
    """
    response = files.download_file(filename)
    return response

@login_required(login_url="login")
def delete_labgroup(request, labgroup_id):
    """
        Delete course from created_labs view.
    """
    if request.user.is_staff:
        labgroup = LabGroups.objects.get(pk=labgroup_id)
        labgroup.deleted = 1
        labgroup.save()

    return redirect(created_labs)


@login_required(login_url="login")
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

@login_required(login_url="login")
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


@login_required(login_url="login")
def archive(request):
    """
        View for rendering archive page
    """
    if request.user.is_staff is not True:
        return redirect("/open_labs")

    users = User.objects.filter(is_staff = False)
    return render(request, "archive.html", {"users":users})

@login_required(login_url="login")
def personal_archive(request, user_id):
    """
        View for individual student's reports
    """
    if request.user.is_staff is not True:
        return redirect("/open_labs")

    student = User.objects.get(pk=user_id)
    filtered_reports = filter_reports.filter_report(user_id)
    all_courses = Courses.objects.all().order_by("id").values()

    return render(request, "personal_archive.html", {"student":student,
                                                     "filtered_reports":filtered_reports,
                                                     "all_courses":all_courses})

@login_required(login_url="login")
def system(request):
    """
        View for system settings
    """
    if request.user.is_superuser is not True:
        return redirect(created_labs)

    return render(request, "system.html")

@login_required(login_url="login")
def instructions(request):
    """
        View for instructions page
    """
    return render(request, "instructions.html")

@login_required(login_url="login")
def user_info(request):
    """
        View for user info page where user can change their email address
    """

    if request.method == "POST":
        new_email = request.POST.get("new_email")
        user = request.user
        users_info.change_email(request, user, new_email)

    return render(request, "user_info.html")

@login_required(login_url="login")
def update_multiple_groups(request):
    """ 
        View for updating labgroups from the same lab shift at the same time
    """

    if request.method == "GET":
        if request.user.is_staff is not True:
            return redirect("/open_labs")

    if request.method == "POST":
        lab_group_ids = request.POST.getlist("lab_groups[]")
        place = request.POST.get("place")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        assistant_id = request.POST.get("assistant")
        assistant = User.objects.get(pk=assistant_id)
        if not date:
            lab_group = LabGroups.objects.get(id=int(lab_group_ids[0]))
            date=lab_group.date
        for lab_group_id in lab_group_ids:
            labgroups.update(date, start_time, end_time, place, assistant, lab_group_id)
        return redirect(created_labs)

    lab_group_ids = request.GET.getlist("lab_groups[]")
    lab_group = LabGroups.objects.get(id=int(lab_group_ids[0]))
    course_id = request.GET.get("course_id")
    course = Courses.objects.get(pk=course_id)

    assistants = User.objects.filter(is_staff=True)

    return render(request, "update_multiple_groups.html",
                            {"lab_group_ids":lab_group_ids,
                            "lab_group":lab_group, 
                            "course":course, "assistants":assistants})
