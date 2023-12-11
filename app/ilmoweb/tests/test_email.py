from django.contrib.auth.hashers import make_password
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from ilmoweb.models import User, Courses, Labs, LabGroups, Report
from ilmoweb.logic import labgroups

class TestEmail(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            student_id = 100111222,
            username = "pvirtanen",
            password = make_password("virtanen"),
            first_name = "Pekka",
            last_name = "Virtanen",
            email = "pekka.virtanen@ilmoweb.fi"
        )
        self.user.save()

        self.assistant = User.objects.create(
            username = "AnttiA",
            password = make_password("assari"),
            first_name = "Antti",
            last_name = "Assari",
            email = "antti.assari@ilmoweb.fi",
            is_staff = True
        )
        self.assistant.save()

        self.course = Courses.objects.create(
            name = "Kemian Labratyö",
            description = "Kemian Labratyö-kurssi",
            labs_amount = 2,
            is_visible = False
        )

        self.superuser = User.objects.create_superuser(
            username = "kemianope",
            password = "atomi123"
        )
        self.superuser.save()

        self.client=Client()

        # visible lab
        self.lab = Labs.objects.create(
            course = self.course,
            name = "Kemian Labratyö-kurssi labra 1",
            description = "Labratyö-kurssin ensimmäinen labra",
            max_students = 20,
            is_visible = True
        )

        # empty labgroup
        self.labgroup = LabGroups.objects.create(
            lab = self.lab,
            date = "2023-06-01",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            status = 0,
            assistant = self.assistant
        )

        # Report
        self.report = Report.objects.create(
            student = self.user,
            lab_group = self.labgroup,
            send_date = "2023-06-10",
            report_file = "raportti.pdf",
            report_status = 1,
            comments = "",
        )
        self.report.save()

    # Tests for changing email address

    def test_user_can_change_their_email(self):
        new_email="testi.meili@ilmo.fi"
        self.client.force_login(self.user)
        response = self.client.post("/user_info/", {"new_email":new_email})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)
    
    def test_cannot_change_email_if_not_logged_in(self):
        new_email="testi.meili@ilmo.fi"
        response = self.client.post("/user_info/", {"new_email":new_email})
        self.assertEqual(response.status_code, 302)
    
    def test_cannot_change_email_if_it_is_not_valid(self):
        new_email="sähköpostiosoite"
        self.client.force_login(self.user)
        response = self.client.post("/user_info/", {"new_email":new_email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.email, "pekka.virtanen@ilmoweb.fi")

    # Tests for email notifications

    def test_confirmation_email(self):
        self.client.force_login(self.user)
        user_id = self.user.id
        group_id = self.labgroup.id
        max_students = self.lab.max_students
        students = self.labgroup.signed_up_students

        response_post = self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})
        response_get = self.client.get("/open_labs/")

        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_get.status_code, 200)

        self.labgroup.refresh_from_db()
        students = self.labgroup.signed_up_students
        self.assertEqual(students, 1)
        
        labgroups.email(self.labgroup, "confirm")

        subject = "Ilmoittautuminen laboratoriotyöhön hyväksytty"
        self.assertEqual(mail.outbox[0].subject, subject)
        message = (
            f"Ilmoittautumisesi laboratoriotyöhön {self.lab.name} on hyväksytty.\n"
            f"Ajankohta: {self.labgroup.date.day}.{self.labgroup.date.month}.{self.labgroup.date.year} "
            f"klo {self.labgroup.start_time.hour} - {self.labgroup.end_time.hour}\n"
            f"Paikka: {self.labgroup.place}\n"
        )
        self.assertEqual(mail.outbox[0].body, message)
        sender = "grp-fyskem-labra-ilmo@helsinki.fi"
        self.assertEqual(mail.outbox[0].from_email, sender)
        recipient = ["pekka.virtanen@ilmoweb.fi"]
        self.assertEqual(mail.outbox[0].to, recipient)

    def test_canceling_email(self):
        self.client.force_login(self.user)
        user_id = self.user.id
        group_id = self.labgroup.id
        max_students = self.lab.max_students
        students = self.labgroup.signed_up_students

        response_post = self.client.post("/open_labs/enroll/", {"max_students":max_students, "students":students, "user_id":user_id, "group_id":group_id})
        response_get = self.client.get("/open_labs/")

        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_get.status_code, 200)

        self.labgroup.refresh_from_db()
        students = self.labgroup.signed_up_students
        self.assertEqual(students, 1)
        
        labgroups.email(self.labgroup, "cancel")

        subject = "Laboratoriotyö peruttu"
        self.assertEqual(mail.outbox[0].subject, subject)
        message = (
            f"Laboratoriotyö "
            f"{self.lab.name} ({self.labgroup.date.day}.{self.labgroup.date.month}.{self.labgroup.date.year}) "
            "on peruttu."
        )
        self.assertEqual(mail.outbox[0].body, message)
        sender = "grp-fyskem-labra-ilmo@helsinki.fi"
        self.assertEqual(mail.outbox[0].from_email, sender)
        recipient = ["pekka.virtanen@ilmoweb.fi"]
        self.assertEqual(mail.outbox[0].to, recipient)
    
    def test_email_when_report_is_graded(self):
        self.client.force_login(self.superuser)
        url = reverse("evaluate_report", args=[str(self.report.id)])
        self.client.post(url, {"grade": 4, "comments": "Nice"})
        subject = "Raporttisi on arvioitu"
        self.assertEqual(mail.outbox[0].subject, subject)
        message = (
            f"Raporttisi työhön {self.lab.name} on arvioitu.\n"
            f"Arviointia pääsee tarkastelemaan palautussovelluksesta."
        )
        self.assertEqual(mail.outbox[0].body, message)
        sender = "grp-fyskem-labra-ilmo@helsinki.fi"
        self.assertEqual(mail.outbox[0].from_email, sender)
        recipient = ["pekka.virtanen@ilmoweb.fi"]
        self.assertEqual(mail.outbox[0].to, recipient)

    def test_email_when_report_is_sent_back_for_fixing(self):
        self.client.force_login(self.superuser)
        url = reverse("evaluate_report", args=[str(self.report.id)])
        self.client.post(url, {"grade": 0, "comments": "Nice"})
        subject = "Raporttisi vaatii korjausta"
        self.assertEqual(mail.outbox[0].subject, subject)
        message = (
            f"Raporttisi työhön {self.lab.name} on arvioitu ja se vaatii korjausta.\n"
            f"Kommentit ja korjausehdotukset löytyvät palautussovelluksesta."
        )
        self.assertEqual(mail.outbox[0].body, message)
        sender = "grp-fyskem-labra-ilmo@helsinki.fi"
        self.assertEqual(mail.outbox[0].from_email, sender)
        recipient = ["pekka.virtanen@ilmoweb.fi"]
        self.assertEqual(mail.outbox[0].to, recipient)