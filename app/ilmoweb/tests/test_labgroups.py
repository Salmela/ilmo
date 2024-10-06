from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User, Courses, Labs, LabGroups, Report
from ilmoweb.logic import labgroups, signup
import datetime

class TestLabGroups(TestCase):
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

        self.superuser1 = User.objects.create_superuser(
            username = "kemianope",
            password = "atomi123"
        )
        self.superuser1.save()

        self.client=Client()

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

#    def test_teacher_can_create_labgroup(self):
#        lab = self.lab1.id
#        date = "2023-10-13"
#        start_time = "08:00"
#        end_time = "12:00"
#        place = "B105"
#        assistant = User.objects.filter(is_staff=True).first()
#
#        self.client.force_login(self.superuser1)
#        prev = len(LabGroups.objects.all())
#        get_response = self.client.get("/create_group/", {"course_id":self.course1.id})
#        self.assertEqual(get_response.status_code, 200)

#        post_response = self.client.post("/create_group/", {"labs[]":lab, "place":place, "date":date, "start_time":start_time, "end_time":end_time, "assistant":assistant.id})
#        self.assertEqual(post_response.status_code, 302)
#        new = len(LabGroups.objects.all())
#        self.assertEqual(prev + 1, new)

#    def test_teacher_can_create_multiple_labgroups(self):
#        labs = [self.lab1.id, self.lab2.id]
#        date = "2023-10-13"
#        start_time = "08:00"
#        end_time = "12:00"
#        place = "B105"
#        assistant = User.objects.filter(is_staff=True).first()

#        self.client.force_login(self.superuser1)
#        prev = len(LabGroups.objects.all())
#        get_response = self.client.get("/create_group/", {"course_id":self.course1.id})
#        self.assertEqual(get_response.status_code, 200)

#        post_response = self.client.post("/create_group/", {"labs[]":labs, "place":place, "date":date, "start_time":start_time, "end_time":end_time, "assistant":assistant.id})
#        self.assertEqual(post_response.status_code, 302)
#        new = len(LabGroups.objects.all())
#        self.assertEqual(prev + 2, new)

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

        self.assertEqual(response_post.status_code, 301)
        self.assertEqual(response_get.status_code, 200)

        self.labgroup1.refresh_from_db()
        students = self.labgroup1.signed_up_students
        self.assertEqual(students, 0)

    def test_student_cannot_enroll_twice_to_same_labgroup(self):
        self.client.force_login(self.user1)
        user_id = self.user1.id,
        group_id = self.labgroup1.id
        max_students = self.lab1.max_students
        students = self.labgroup1.signed_up_students

        self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})

        response_post = self.client.post("/open_labs/enroll", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})

        self.assertEqual(response_post.status_code, 301)

        self.labgroup1.refresh_from_db()
        students = self.labgroup1.signed_up_students
        self.assertEqual(students, 1)

    # Tests for confirming labgroup

    def test_teacher_can_confirm_nonempty_labgroup(self):
        self.client.force_login(self.superuser1)
        groups = [self.labgroup2.id]
        response_post = self.client.post("/created_labs/confirm/", {"lab_groups": groups})

        self.assertEqual(response_post.status_code, 302)

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

        response = self.client.post("/created_labs/confirm/", {"lab_groups": groups})

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(str(messages[0]), "Tyhjää ryhmää ei voida vahvistaa")

        self.labgroup1.refresh_from_db()
        status = self.labgroup1.status
        self.assertEqual(status, 0)

    def test_student_cannot_confirm_labgroup(self):
        self.client.force_login(self.user1)
        groups = [self.labgroup1.id]

        self.client.post("/created_labs/confirm/", {"lab_group_id": groups})

        self.labgroup1.refresh_from_db()
        status = self.labgroup1.status
        self.assertEqual(status, 0)

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
        response = self.client.post(url, {"lab_groups":lab_groups})
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.status, 1)
        self.assertRedirects(response, reverse("created_labs"))

    def test_teacher_can_cancel_and_republish_labgroup(self):
        self.client.force_login(self.superuser1)
        lab_groups = [self.labgroup2.id]
        url = reverse("labgroup_status")
        response = self.client.post(url, {"lab_groups":lab_groups})
        self.assertEqual(response.status_code, 302)
        self.labgroup2.refresh_from_db()
        self.assertEqual(self.labgroup2.status, 3)
        url_2 = reverse("labgroup_status")
        response_2 = self.client.post(url_2, {"lab_groups":lab_groups})
        self.assertEqual(response_2.status_code, 302)
        self.labgroup2.refresh_from_db()
        self.assertEqual(self.labgroup2.status, 1)
        self.assertRedirects(response, reverse("created_labs"))

    def test_student_cannot_publish_labgroup(self):
        lab_groups = [self.labgroup1.id]
        self.client.force_login(self.user1)
        url = reverse("labgroup_status")
        response = self.client.post(url, {"lab_groups":lab_groups})
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.status, 0)

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

    def test_staff_get_request_returns_update_multiple_groups_template(self):
        self.client.force_login(self.assistant1)

        data = {
            "lab_groups[]": [str(self.labgroup1.id)],
            "course_id": str(self.course1.id),
        }
        response = self.client.get(reverse("update_multiple_groups"), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_multiple_groups.html")

        self.assertEqual(response.context["lab_group_ids"], [str(self.labgroup1.id)])
        self.assertEqual(response.context["lab_group"], self.labgroup1)
        self.assertEqual(response.context["course"], self.course1)
