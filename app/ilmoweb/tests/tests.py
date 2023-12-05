from django.contrib.auth.hashers import make_password, check_password
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User, Courses, Labs, LabGroups, Report, TeachersMessage
from ilmoweb.logic import labgroups, signup, filter_reports, teachermessage
import datetime

class FirstTest(TestCase):
    def setUp(self):
        self.testApp = "IlmoWeb"

    def test_mock_test(self):
        self.assertEqual(self.testApp, "IlmoWeb")

class TestModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            student_id = 100111222,
            username = "pvirtanen",
            password = make_password("virtanen"),
            first_name = "Pekka",
            last_name = "Virtanen",
            email = "pekka.virtanen@ilmoweb.fi"
        )
        self.user1.save()

        self.assistant1 = User.objects.create(
            username = "AnttiA",
            password = make_password("assari"),
            first_name = "Antti",
            last_name = "Assari",
            email = "antti.assari@ilmoweb.fi",
            is_staff = True
        )
        self.assistant1.save()

        self.assistant2 = User.objects.create(
            username = "AinoA",
            password = make_password("assari2"),
            first_name = "Aino",
            last_name = "Assari",
            email = "aino.assari2@ilmoweb.fi",
            is_staff = True
        )
        self.assistant2.save()

        self.course1 = Courses.objects.create(
            name = "Kemian Labratyö",
            description = "Kemian Labratyö-kurssi",
            labs_amount = 2,
            is_visible = False
        )

        # visible lab
        self.lab1 = Labs.objects.create(
            course = self.course1,
            name = "Kemian Labratyö-kurssi labra 1",
            description = "Labratyö-kurssin ensimmäinen labra",
            max_students = 20,
            is_visible = True
        )

        # invisible lab
        self.lab2 = Labs.objects.create(
            course = self.course1,
            name = "Kemian Labratyö-kurssi labra 2",
            description = "Labratyö-kurssin toinen labra",
            max_students = 20,
            is_visible = False
        )

        # empty labgroup
        self.labgroup1 = LabGroups.objects.create(
            lab = self.lab1,
            date = "2023-06-01",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            status = 0,
            assistant = self.assistant1
        )

        # nonempty labgroup
        self.labgroup2 = LabGroups.objects.create(
            lab = self.lab1,
            date = "2023-06-02",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            status = 1,
            signed_up_students = 1
        )

        # Report for testing
        self.report1 = Report.objects.create(
            student = self.user1,
            lab_group = self.labgroup1,
            send_date = "2023-06-10",
            report_file = "raportti.pdf",
            report_status = 1,
            comments = "",
        )
        self.report1.save()

        # creating a superuser for testing login
        self.superuser1 = User.objects.create_superuser(
            username = "kemianope",
            password = "atomi123"
        )
        self.superuser1.save()

        self.client=Client()

        # Report for testing report filtering
        self.report2 = Report.objects.create(
            student = self.user1,
            lab_group = self.labgroup1,
            send_date = "2023-06-11",
            report_file = "raportti2.pdf",
            report_status = 3,
            comments = "",
        )
        self.report2.save()


    # Tests for User-model
    
    def test_user_is_created_with_correct_id(self):
        self.assertEqual(self.user1.student_id, 100111222)

    def test_user_is_created_with_correct_username(self):
        self.assertEqual(self.user1.username, "pvirtanen")

    def test_user_is_created_with_correct_password(self):
        self.assertTrue(check_password("virtanen", self.user1.password))

    def test_user_is_created_with_correct_name(self):
        self.assertEqual(self.user1.first_name, "Pekka")

    def test_user_is_created_with_correct_surname(self):
        self.assertEqual(self.user1.last_name, "Virtanen")

    def test_user_is_created_with_correct_email(self):
        self.assertEqual(self.user1.email, "pekka.virtanen@ilmoweb.fi")

    # Tests for Courses-model

    def test_course_is_created_with_correct_name(self):
        self.assertEqual(self.course1.name, "Kemian Labratyö")

    def test_course_is_created_with_correct_description(self):
        self.assertEqual(self.course1.description, "Kemian Labratyö-kurssi")

    def test_course_is_created_with_correct_labs_amount(self):
        self.assertEqual(self.course1.labs_amount, 2)

    def test_course_is_created_with_correct_is_visible_value(self):
        self.assertFalse(self.course1.is_visible)

    # Tests for Labs-model

    def test_lab_is_created_with_correct_name(self):
        self.assertEqual(self.lab1.course, self.course1)

    def test_lab_is_created_with_correct_name(self):
        self.assertEqual(self.lab1.name, "Kemian Labratyö-kurssi labra 1")

    def test_lab_is_created_with_correct_description(self):
        self.assertEqual(self.lab1.description, "Labratyö-kurssin ensimmäinen labra")

    def test_lab_is_created_with_correct_max_students_value(self):
        self.assertEqual(self.lab1.max_students, 20)

    def test_lab_is_created_with_correct_is_visible_value(self):
        self.assertTrue(self.lab1.is_visible)

    # Tests for LabGroups

    def test_lab_group_is_created_with_correct_lab(self):
        self.assertEqual(self.labgroup1.lab, self.lab1)

    def test_lab_group_is_created_with_correct_date(self):
        self.assertEqual(self.labgroup1.date, "2023-06-01")

    def test_lab_group_is_created_with_correct_start_time(self):
        self.assertEqual(self.labgroup1.start_time, "14:30")

    def test_lab_group_is_created_with_correct_end_time(self):
        self.assertEqual(self.labgroup1.end_time, "16:30")

    def test_lab_group_is_created_with_correct_place(self):
        self.assertEqual(self.labgroup1.place, "Chemicum")

    def test_lab_group_is_created_with_correct_is_visible_value(self):
        self.assertEqual(self.labgroup1.status, 0)
    
    def test_lab_group_is_created_with_correct_assistant(self):
        self.assertEqual(self.labgroup1.assistant, self.assistant1)

    # Tests for logging in as superuser

    def test_login_for_superuser(self):
        logged_in = self.client.login(username="kemianope", password="atomi123")
        self.assertTrue(logged_in)

    def test_login_with_wrong_password(self):
        logged_in = self.client.login(username="kemianope", password="chemicum")
        self.assertFalse(logged_in)

    def test_login_as_not_superuser(self):
        logged_in = self.client.login(username=self.user1.username, password=self.user1.password)
        self.assertFalse(logged_in)

    def test_respond_with_correct_status_code_login(self):
        response_get = self.client.get("/accounts/login/",
                                    {"username":"kemianope", "password":"atomi123"})
        status_code_get = response_get.status_code
        self.assertEqual(status_code_get, 200) # 200 OK

        response_post = self.client.post("/accounts/login/",
                                    {"username":"kemianope", "password":"atomi123"})
        status_code_post = response_post.status_code
        self.assertEqual(status_code_post, 302) # 302 Found

    def test_logout(self):
        logged_in = self.client.login(username="kemianope", password="atomi123")
        logged_in = self.client.logout()
        self.assertFalse(logged_in)

    def test_respond_with_correct_status_code_logout(self):
        response_get = self.client.get("/accounts/logout/",
                                    {"username":"kemianope", "password":"atomi123"})
        status_code_get = response_get.status_code
        self.assertEqual(status_code_get, 302) # 302 Found

    def test_navigate_to_right_page_after_login_as_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("home"))
        
        self.assertRedirects(response, reverse('open_labs'))
        
    def test_navigate_to_right_page_after_login_as_staff(self):
        self.client.force_login(self.assistant1)
        response = self.client.get(reverse("home"))
        
        self.assertRedirects(response, reverse('created_labs'))

    def test_logged_out_user_gets_home_page(self):
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_student_can_not_get_to_created_labs(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('created_labs'))
        self.assertEqual(response.url, '/open_labs')
        self.assertEqual(response.status_code, 302)

    # Tests for labgroup enrollment

    def test_student_can_enroll_to_labgroup(self):
        self.client.force_login(self.user1)
        user_id = self.user1.id,
        group_id = self.labgroup1.id
        max_students = self.lab1.max_students
        students = self.labgroup1.signed_up_students

        response_post = self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})
        response_get = self.client.get("/open_labs/")

        # correct status codes

        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_get.status_code, 200)

        # check database

        self.labgroup1.refresh_from_db()
        students = self.labgroup1.signed_up_students
        self.assertEqual(students, 1)
        
    def test_enrollment_gives_success_message(self):
        self.client.force_login(self.user1)
        user_id = self.user1.id,
        group_id = self.labgroup1.id
        max_students = self.lab1.max_students
        students = self.labgroup1.signed_up_students

        response_post = self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})
        messages = [m.message for m in get_messages(response_post.wsgi_request)]
        self.assertEqual(str(messages[0]), "Ilmoittautuminen onnistui!")
    
    def test_teacher_cannot_enroll_to_labgroup(self):
        self.client.force_login(self.superuser1)
        user_id = self.user1.id,
        group_id = self.labgroup1.id
        max_students = self.lab1.max_students
        students = self.labgroup1.signed_up_students

        response_post = self.client.post("/open_labs/enroll", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})
        response_get = self.client.get("/open_labs/")

        # correct status codes

        self.assertEqual(response_post.status_code, 301)
        self.assertEqual(response_get.status_code, 200)

        # check database

        self.labgroup1.refresh_from_db()
        students = self.labgroup1.signed_up_students
        self.assertEqual(students, 0)
    
    def test_student_cannot_enroll_twice_to_same_labgroup(self):
        self.client.force_login(self.user1)
        user_id = self.user1.id,
        group_id = self.labgroup1.id
        max_students = self.lab1.max_students
        students = self.labgroup1.signed_up_students

        # student enrolls
        self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})

        # same student enrolls again
        response_post = self.client.post("/open_labs/enroll", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})

        # correct status code

        self.assertEqual(response_post.status_code, 301)

        # database only has one signed up student
        self.labgroup1.refresh_from_db()
        students = self.labgroup1.signed_up_students
        self.assertEqual(students, 1)

    # Tests for confirming labgroup
    
    def test_teacher_can_confirm_nonempty_labgroup(self):
        self.client.force_login(self.superuser1)
        groups = [self.labgroup2.id]
        response_post = self.client.post("/created_labs/confirm/", {"lab_groups": groups})
        
        # correct status code
        self.assertEqual(response_post.status_code, 302)

        # check database update
        self.labgroup2.refresh_from_db()
        status = self.labgroup2.status
        self.assertEqual(status, 2)

    def test_confirming_groups_gives_succeess_message(self):
        self.client.force_login(self.superuser1)
        groups = [self.labgroup2.id]
        response_post = self.client.post("/created_labs/confirm/", {"lab_groups": groups})

        messages = [m.message for m in get_messages(response_post.wsgi_request)]
        self.assertEqual(str(messages[0]), "Ryhmä vahvistettu")
    

    def test_teacher_cannot_confirm_empty_labgroup(self):
        self.client.force_login(self.superuser1)
        groups = [self.labgroup1.id]

        # try to confirm
        response = self.client.post("/created_labs/confirm/", {"lab_groups": groups})

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(str(messages[0]), "Tyhjää ryhmää ei voida vahvistaa")
        
        # check database stays same
        self.labgroup1.refresh_from_db()
        status = self.labgroup1.status
        self.assertEqual(status, 0)

    def test_student_cannot_confirm_labgroup(self):
        self.client.force_login(self.user1)
        groups = [self.labgroup1.id]

        # try to confirm
        self.client.post("/created_labs/confirm/", {"lab_group_id": groups})
        
        # check database stays same
        self.labgroup1.refresh_from_db()
        status = self.labgroup1.status
        self.assertEqual(status, 0)

    # Tests for reports
    def test_report_is_saved_to_db(self):
        self.all_reports = Report.objects.all()
        self.assertEqual(len(self.all_reports), 2)

    def test_saved_report_has_correct_fields(self):
        self.all_reports = Report.objects.all()
        self.assertEqual(self.all_reports[0].student, self.user1)
        self.assertEqual(self.all_reports[0].lab_group, self.labgroup1)
        self.assertEqual(self.all_reports[0].report_file, "raportti.pdf")
        self.assertEqual(self.all_reports[0].comments, "")
        self.assertEqual(self.all_reports[0].graded_by, None)
    
    # Tests for creating labgroups

    def test_start_end_times_8_to_12(self):
        lab = self.lab1
        date = "2023-10-13"
        start_time = "08:00"
        end_time = "12:00"
        place = "B105"

        labgroups.create(lab, date, start_time, end_time, place, self.assistant1)

        group = LabGroups.objects.get(lab=lab, date=date, place=place)

        self.assertEqual(group.start_time.hour, 8)
        self.assertEqual(group.end_time.hour, 12)

    def test_start_end_times_12_to_16(self):
        lab = self.lab1
        date = "2023-10-13"
        start_time = "12:00"
        end_time = "16:00"
        place = "B105"

        labgroups.create(lab, date, start_time, end_time, place, self.assistant1)

        group = LabGroups.objects.get(lab=lab, date=date, place=place)

        self.assertEqual(group.start_time.hour, 12)
        self.assertEqual(group.end_time.hour, 16)
    
    def test_labgroup_is_saved_to_db(self):
        lab = self.lab1
        date = "2023-10-13"
        start_time = "08:00"
        end_time = "16:00"
        place = "B105"

        prev = len(LabGroups.objects.all())
        labgroups.create(lab, date, start_time, end_time, place, self.assistant1)
        new = len(LabGroups.objects.all())

        self.assertEqual(prev + 1, new)
    
    def test_teacher_can_create_labgroup(self):
        lab = self.lab1.id
        date = "2023-10-13"
        start_time = "08:00"
        end_time = "12:00"
        place = "B105"
        assistant = User.objects.filter(is_staff=True).first()

        self.client.force_login(self.superuser1)
        prev = len(LabGroups.objects.all())
        get_response = self.client.get("/create_group/", {"course_id":self.course1.id})
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post("/create_group/", {"labs[]":lab, "place":place, "date":date, "start_time":start_time, "end_time":end_time, "assistant":assistant.id})
        self.assertEqual(post_response.status_code, 302)
        new = len(LabGroups.objects.all())
        self.assertEqual(prev + 1, new)

    def test_teacher_can_create_multiple_labgroups(self):
        labs = [self.lab1.id, self.lab2.id]
        date = "2023-10-13"
        start_time = "08:00"
        end_time = "12:00"
        place = "B105"
        assistant = User.objects.filter(is_staff=True).first()

        self.client.force_login(self.superuser1)
        prev = len(LabGroups.objects.all())
        get_response = self.client.get("/create_group/", {"course_id":self.course1.id})
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post("/create_group/", {"labs[]":labs, "place":place, "date":date, "start_time":start_time, "end_time":end_time, "assistant":assistant.id})
        self.assertEqual(post_response.status_code, 302)
        new = len(LabGroups.objects.all())
        self.assertEqual(prev + 2, new)
    
    def test_student_cannot_access_create_labgroup(self):
        self.client.force_login(self.user1)

        response = self.client.get("/create_group/", {"course_id":self.course1.id})
        self.assertEqual(response.url, "/open_labs")
    
    def test_cannot_create_labgroup_if_not_logged_in(self):
        lab = self.lab1.id
        date = "2023-10-13"
        start_time = "08:00"
        end_time = "12:00"
        place = "B105"

        prev = len(LabGroups.objects.all())
        post_response = self.client.post("/create_group/", {"labs[]":lab, "place":place, "date":date, "start_time":start_time, "end_time":end_time})
        self.assertEqual(post_response.status_code, 302)
        new = len(LabGroups.objects.all())
        self.assertEqual(prev, new)

    # Tests for activating labs

    def test_teacher_can_activate_lab(self):
        self.client.force_login(self.superuser1)
        url = reverse("make_lab_visible", args=[str(self.lab2.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab2.refresh_from_db()
        self.assertEqual(self.lab2.is_visible, True)
    
    def test_teacher_can_deactivate_lab(self):
        self.client.force_login(self.superuser1)
        url = reverse("make_lab_visible", args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.is_visible, False)
    
    def test_student_cannot_activate_lab(self):
        self.client.force_login(self.user1)
        url = reverse("make_lab_visible", args=[str(self.lab2.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab2.refresh_from_db()
        self.assertEqual(self.lab2.is_visible, False)

    # Tests for deleting labs

    def test_teacher_can_delete_lab(self):
        self.client.force_login(self.superuser1)
        url = reverse("delete_lab", args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.deleted, True)
    
    def test_student_cannot_delete_lab(self):
        self.client.force_login(self.user1)
        url = reverse("delete_lab", args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.deleted, False)

    # Tests for evaluating reports

    def test_teacher_can_evaluate_reports(self):
        self.client.force_login(self.superuser1)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        pdf = SimpleUploadedFile("comments.pdf", b"comment", content_type="application/pdf")
        response = self.client.post(url, {"grade": 5, "comments": "Perfectly done!", "file": pdf})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.grade, 5)
        self.assertEqual(self.report1.comments, "Perfectly done!")
        self.assertIsNotNone(self.report1.comment_file)
        self.assertEqual(self.report1.comment_file_name, "comments.pdf")
        self.assertEqual(self.report1.graded_by_id, self.superuser1.id)
        self.assertEqual(self.report1.grading_date, datetime.date.today())
        self.assertEqual(self.report1.report_status, 4)

    def test_teacher_can_evaluate_without_comment(self):
        self.client.force_login(self.superuser1)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        response = self.client.post(url, {"grade": 3, "comments": ""})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.grade, 3)
        self.assertEqual(self.report1.comments, "")
        self.assertEqual(self.report1.graded_by_id, self.superuser1.id)
        self.assertEqual(self.report1.grading_date, datetime.date.today())
        self.assertEqual(self.report1.report_status, 4)
    
    def test_student_cannot_grade_reports(self):
        self.client.force_login(self.user1)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        response = self.client.post(url, {"grade": 5, "comments": "Perfectly done!"})
        self.assertEqual(response.url, "/my_labs")
    
    def test_teacher_can_send_reports_to_be_fixed(self):
        self.client.force_login(self.superuser1)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        response = self.client.post(url, {"grade": 0, "comments": "Fix the report"})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.report_status, 2)
        self.assertEqual(self.report1.comments, "Fix the report")

    # Tests for deleting labgroups

    def test_teacher_can_delete_labgroup(self):
        self.client.force_login(self.superuser1)
        url = reverse("delete_labgroup", args=[str(self.labgroup1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.deleted, True)

    def test_student_cannot_delete_labgroup(self):
        self.client.force_login(self.user1)
        url = reverse("delete_labgroup", args=[str(self.labgroup1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.deleted, False)
        self.client.force_login(self.user1)
        signup.signup(self.user1, self.labgroup1)

    # Test for cancelling enrollment

    def test_student_can_cancel_enrollment(self):
        self.client.force_login(self.user1)
        signup.signup(self.user1, self.labgroup1)
        self.assertEqual(self.labgroup1.signed_up_students, 1)
        url = reverse("cancel_enrollment", args=[str(self.labgroup1.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.signed_up_students, 0)

    def test_cancelling_enrollment_gives_success_message(self):
        self.client.force_login(self.user1)
        signup.signup(self.user1, self.labgroup1)
        self.assertEqual(self.labgroup1.signed_up_students, 1)
        url = reverse("cancel_enrollment", args=[str(self.labgroup1.id)])
        response = self.client.post(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(str(messages[0]), "Ilmoittautuminen peruutettu")

    def test_staff_can_not_cancel_enrollment(self):
        self.client.force_login(self.assistant1)
        url = reverse("cancel_enrollment", args=[str(self.labgroup1.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
    
    # Tests for publishing/canceling labgroups

    def test_teacher_can_publish_labgroup(self):
        self.client.force_login(self.superuser1)
        lab_groups = [self.labgroup1.id]
        url = reverse("labgroup_status")
        response = self.client.post(url, {'lab_groups':lab_groups})
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.status, 1)
        self.assertRedirects(response, reverse('created_labs'))
    
    def test_teacher_can_cancel_and_republish_labgroup(self):
        self.client.force_login(self.superuser1)
        lab_groups = [self.labgroup2.id]
        url = reverse("labgroup_status")
        response = self.client.post(url, {'lab_groups':lab_groups})
        self.assertEqual(response.status_code, 302)
        self.labgroup2.refresh_from_db()
        self.assertEqual(self.labgroup2.status, 3)
        url_2 = reverse("labgroup_status")
        response_2 = self.client.post(url_2, {'lab_groups':lab_groups})
        self.assertEqual(response_2.status_code, 302)
        self.labgroup2.refresh_from_db()
        self.assertEqual(self.labgroup2.status, 1)
        self.assertRedirects(response, reverse('created_labs'))
    
    def test_student_cannot_publish_labgroup(self):
        lab_groups = [self.labgroup1.id]
        self.client.force_login(self.user1)
        url = reverse("labgroup_status")
        response = self.client.post(url, {'lab_groups':lab_groups})
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.status, 0)

    def test_get_request_redirects_to_created_labs(self):
        self.client.force_login(self.superuser1)
        response = self.client.get(reverse('labgroup_status'))
        self.assertRedirects(response, reverse('created_labs'))
    
    # Tests for updating labgroups

    def test_teacher_can_update_labgroups(self):
        date = "2024-11-11"
        start_time = "8:00"
        end_time = "12:00"
        place = "B105"
        assistant = self.assistant2

        self.client.force_login(self.superuser1)
        url = reverse("update_group", args=[str(self.labgroup1.id)])
        response = self.client.post(url, {"date": date, "start_time":start_time, "end_time":end_time, "place":place, "assistant":assistant.id})
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.date, datetime.date(2024, 11, 11))
        self.assertEqual(self.labgroup1.start_time, datetime.time(8))
        self.assertEqual(self.labgroup1.end_time, datetime.time(12))
        self.assertEqual(self.labgroup1.place, "B105")
        self.assertEqual(self.labgroup1.assistant.username, "AinoA")
    
    def test_student_cannot_update_labgroups(self):
        self.client.force_login(self.user1)
        url = reverse("update_group", args=[str(self.labgroup1.id)])
        response = self.client.get(url)
        self.assertEqual(response.url, "/open_labs" )
        self.assertEqual(self.labgroup1.place, "Chemicum")

    # Tests for changing email address

    def test_user_can_change_their_email(self):
        new_email="testi.meili@ilmo.fi"
        self.client.force_login(self.user1)
        response = self.client.post("/user_info/", {"new_email":new_email})
        self.assertEqual(response.status_code, 200)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, new_email)
    
    def test_cannot_change_email_if_not_logged_in(self):
        new_email="testi.meili@ilmo.fi"
        response = self.client.post("/user_info/", {"new_email":new_email})
        self.assertEqual(response.status_code, 302)
    
    def test_cannot_change_email_if_it_is_not_valid(self):
        new_email="sähköpostiosoite"
        self.client.force_login(self.user1)
        response = self.client.post("/user_info/", {"new_email":new_email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user1.email, "pekka.virtanen@ilmoweb.fi")

    # Tests for email notifications

    def test_confirmation_email(self):
        self.client.force_login(self.user1)
        user_id = self.user1.id
        group_id = self.labgroup1.id
        max_students = self.lab1.max_students
        students = self.labgroup1.signed_up_students

        response_post = self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})
        response_get = self.client.get("/open_labs/")

        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_get.status_code, 200)

        self.labgroup1.refresh_from_db()
        students = self.labgroup1.signed_up_students
        self.assertEqual(students, 1)
        
        labgroups.email(self.labgroup1, "confirm")

        subject = "Ilmoittautuminen laboratoriotyöhön hyväksytty"
        self.assertEqual(mail.outbox[0].subject, subject)
        message = (
            f"Ilmoittautumisesi laboratoriotyöhön {self.lab1.name} on hyväksytty.\n"
            f"Ajankohta: {self.labgroup1.date.day}.{self.labgroup1.date.month}.{self.labgroup1.date.year} "
            f"klo {self.labgroup1.start_time.hour} - {self.labgroup1.end_time.hour}\n"
            f"Paikka: {self.labgroup1.place}\n"
        )
        self.assertEqual(mail.outbox[0].body, message)
        sender = "grp-fyskem-labra-ilmo@helsinki.fi"
        self.assertEqual(mail.outbox[0].from_email, sender)
        recipient = ["pekka.virtanen@ilmoweb.fi"]
        self.assertEqual(mail.outbox[0].to, recipient)

    def test_canceling_email(self):
        self.client.force_login(self.user1)
        user_id = self.user1.id
        group_id = self.labgroup1.id
        max_students = self.lab1.max_students
        students = self.labgroup1.signed_up_students

        response_post = self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})
        response_get = self.client.get("/open_labs/")

        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_get.status_code, 200)

        self.labgroup1.refresh_from_db()
        students = self.labgroup1.signed_up_students
        self.assertEqual(students, 1)
        
        labgroups.email(self.labgroup1, "cancel")

        subject = "Laboratoriotyö peruttu"
        self.assertEqual(mail.outbox[0].subject, subject)
        message = (
            f"Laboratoriotyö "
            f"{self.lab1.name} ({self.labgroup1.date.day}.{self.labgroup1.date.month}.{self.labgroup1.date.year}) "
            "on peruttu."
        )
        self.assertEqual(mail.outbox[0].body, message)
        sender = "grp-fyskem-labra-ilmo@helsinki.fi"
        self.assertEqual(mail.outbox[0].from_email, sender)
        recipient = ["pekka.virtanen@ilmoweb.fi"]
        self.assertEqual(mail.outbox[0].to, recipient)
    
    # Test for updating multiple lab groups

    def test_teacher_can_update_multiple_labgroups(self):
        labgroup_id_list = [self.labgroup1.id, self.labgroup2.id]
        date = "2023-12-12"
        start_time = "10:00"
        end_time = "15:00"
        place = "D211 (Phy)"
        assistant = self.assistant2.id

        self.client.force_login(self.superuser1)
        response = self.client.post("/update_multiple_groups/", {
            "lab_groups[]":labgroup_id_list,"date":date,
            "start_time":start_time, "end_time":end_time,
            "place":place, "assistant":assistant
        })
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.date, datetime.date(2023, 12, 12))
        self.assertEqual(self.labgroup1.start_time, datetime.time(10))
        self.assertEqual(self.labgroup1.end_time, datetime.time(15))
        self.assertEqual(self.labgroup1.place, "D211 (Phy)")
        self.assertEqual(self.labgroup1.assistant.username, "AinoA")

        self.labgroup2.refresh_from_db()
        self.assertEqual(self.labgroup2.date, datetime.date(2023, 12, 12))
        self.assertEqual(self.labgroup2.start_time, datetime.time(10))
        self.assertEqual(self.labgroup2.end_time, datetime.time(15))
        self.assertEqual(self.labgroup2.place, "D211 (Phy)")
        self.assertEqual(self.labgroup2.assistant.username, "AinoA")

    # Test that user has two reports when they are not filtered
    def test_reports_are_saved_for_same_student(self):
        reports = Report.objects.filter(student=self.user1)
        self.assertEqual(len(reports), 2)

    # Test filter_reports function returns report with highest status per labgroup
    def test_filter_reports_returns_correct_report(self):
        filtered_reports = filter_reports.filter_report(self.user1.id)
        self.assertEqual(filtered_reports[0].report_file, "raportti2.pdf")

    def test_filter_reports_returns_correct_report_when_adding_new(self):
        self.report3 = Report.objects.create(
            student = self.user1,
            lab_group = self.labgroup1,
            send_date = "2023-06-11",
            report_file = "raportti3.pdf",
            report_status = 4,
            comments = "",
        )
        self.report3.save()
        filtered_reports = filter_reports.filter_report(self.user1.id)
        self.assertEqual(filtered_reports[0].report_file, "raportti3.pdf")

    # Filter_reports should only return one report with the highest status
    def test_filter_reports_returns_correct_amount_of_reports(self):
        self.report4 = Report.objects.create(
            student = self.user1,
            lab_group = self.labgroup1,
            send_date = "2023-06-12",
            report_status = 0,
            comments = "",
        )
        self.report4.save()
        filtered_reports = filter_reports.filter_report(self.user1.id)
        self.assertEqual(len(filtered_reports), 1)

    # Tests for teachers message to students
    def message_is_saved_in_database(self):
        self.message = TeachersMessage.objects.create(
            message = "Hello students"
        )

        self.message.save()
        get_message = TeachersMessage.objects.get(id=0)

        self.assertEqual(get_message, "Hello students")
    
    def test_messages_are_updated(self):
        self.message = TeachersMessage.objects.create(
            message = "Hello students"
        )

        self.message.save()

        self.client.force_login(self.superuser1)

        new_message="Hi students"
        response = self.client.post("/teachers_message/", {"message":new_message})
        self.assertEqual(response.status_code, 302)

        self.message.refresh_from_db()

        self.assertEqual(self.message.message, "Hi students")

    def test_student_can_not_get_to_system_page_to_update_message(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('teachers_message'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/open_labs')
    
    # Test for adding notes to a report

    def test_teacher_can_add_notes_to_a_report(self):
        notes = "this is a noteworthy thing"
        self.client.force_login(self.assistant1)
        url = reverse("report_notes", args=[str(self.report1.id)])
        response = self.client.post(url, {"notes":notes})
        self.assertEqual(response.status_code, 302)

        self.report1.refresh_from_db()
        self.assertEqual(self.report1.notes, "this is a noteworthy thing")
    
    def test_student_cannot_add_notes_to_a_report(self):
        notes = "this is a noteworthy thing"
        self.client.force_login(self.user1)
        url = reverse("report_notes", args=[str(self.report1.id)])
        response = self.client.post(url, {"notes":notes})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/my_labs")

        self.report1.refresh_from_db()
        self.assertEqual(self.report1.notes, "")

    # Tests for creating labs

    def test_student_can_not_get_create_lab_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('create_lab'))

        self.assertEqual(response.url, '/open_labs')
        self.assertEqual(response.status_code, 302)

    def test_post_request_creates_new_lab_and_redirects(self):
        self.client.force_login(self.superuser1)

        data = {
            'lab_name': 'Lab',
            'description': 'Lab description',
            'max_students': str(5),
            'course_id': self.course1.id
        }
        response = self.client.post(reverse('create_lab'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('created_labs'))

    def test_staff_gets_correct_template(self):
        self.client.force_login(self.superuser1)
        response = self.client.get(reverse('create_lab'))
        self.assertTemplateUsed(response, 'create_lab.html')

    # Tests for system page
    def test_only_super_user_gets_system_page(self):
        self.client.force_login(self.user1)
        response_user = self.client.get(reverse('system'))
        self.assertEqual(response_user.status_code, 302)
        self.assertEqual(response_user.url, '/open_labs/')
        self.client.logout()

        self.client.force_login(self.assistant1)
        response_staff = self.client.get(reverse('system'))
        self.assertEqual(response_staff.status_code, 302)
        self.assertEqual(response_staff.url, '/created_labs/')
        self.client.logout()

        self.client.force_login(self.superuser1)
        response_superuser = self.client.get(reverse('system'))
        self.assertTemplateUsed(response_superuser, 'system.html')

    # Tests for my labs page
    def test_user_can_access_my_labs(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('my_labs'))
        self.assertEqual(response.status_code, 200)