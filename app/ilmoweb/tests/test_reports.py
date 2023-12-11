from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User, Courses, Labs, LabGroups, Report
from ilmoweb.logic import filter_reports
import datetime

class TestReports(TestCase):
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

        # Report for testing
        self.report1 = Report.objects.create(
            student = self.user,
            lab_group = self.labgroup,
            send_date = "2023-06-10",
            report_file = "raportti.pdf",
            report_status = 1,
            comments = "",
        )
        self.report1.save()

        # Report for testing report filtering
        self.report2 = Report.objects.create(
            student = self.user,
            lab_group = self.labgroup,
            send_date = "2023-06-11",
            report_file = "raportti2.pdf",
            report_status = 3,
            comments = "",
        )
        self.report2.save()

    # Tests for returning report

    def test_get_request_redirects_to_home_page(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("return_report"))
        self.assertEqual(response.url, "/")
        self.assertEqual(response.status_code, 302)

    def test_return_report_with_success(self):
        self.client.force_login(self.user)
        url = reverse("return_report")
        pdf = SimpleUploadedFile("report.pdf", b"report", content_type="application/pdf")
        response = self.client.post(url, {"lab_group_id": self.labgroup.id, "file":pdf})
        self.assertEqual(response.status_code, 302)
    # Tests for evaluating reports

    def test_teacher_can_evaluate_reports(self):
        self.client.force_login(self.superuser)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        pdf = SimpleUploadedFile("comments.pdf", b"comment", content_type="application/pdf")
        response = self.client.post(url, {"grade": 5, "comments": "Perfectly done!", "file": pdf})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.grade, 5)
        self.assertEqual(self.report1.comments, "Perfectly done!")
        self.assertIsNotNone(self.report1.comment_file)
        self.assertEqual(self.report1.comment_file_name, "comments.pdf")
        self.assertEqual(self.report1.graded_by_id, self.superuser.id)
        self.assertEqual(self.report1.grading_date, datetime.date.today())
        self.assertEqual(self.report1.report_status, 4)

    def test_teacher_can_evaluate_without_comment(self):
        self.client.force_login(self.superuser)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        response = self.client.post(url, {"grade": 3, "comments": ""})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.grade, 3)
        self.assertEqual(self.report1.comments, "")
        self.assertEqual(self.report1.graded_by_id, self.superuser.id)
        self.assertEqual(self.report1.grading_date, datetime.date.today())
        self.assertEqual(self.report1.report_status, 4)
    
    def test_student_cannot_grade_reports(self):
        self.client.force_login(self.user)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        response = self.client.post(url, {"grade": 5, "comments": "Perfectly done!"})
        self.assertEqual(response.url, "/my_labs")
    
    def test_teacher_can_send_reports_to_be_fixed(self):
        self.client.force_login(self.superuser)
        url = reverse("evaluate_report", args=[str(self.report1.id)])
        response = self.client.post(url, {"grade": 0, "comments": "Fix the report"})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.report_status, 2)
        self.assertEqual(self.report1.comments, "Fix the report")

    # Test that user has two reports when they are not filtered
    def test_reports_are_saved_for_same_student(self):
        reports = Report.objects.filter(student=self.user)
        self.assertEqual(len(reports), 2)

    # Test filter_reports function returns report with highest status per labgroup
    def test_filter_reports_returns_correct_report(self):
        filtered_reports = filter_reports.filter_report(self.user.id)
        self.assertEqual(filtered_reports[0].report_file, "raportti2.pdf")

    def test_filter_reports_returns_correct_report_when_adding_new(self):
        self.report3 = Report.objects.create(
            student = self.user,
            lab_group = self.labgroup,
            send_date = "2023-06-11",
            report_file = "raportti3.pdf",
            report_status = 4,
            comments = "",
        )
        self.report3.save()
        filtered_reports = filter_reports.filter_report(self.user.id)
        self.assertEqual(filtered_reports[0].report_file, "raportti3.pdf")

    # Filter_reports should only return one report with the highest status
    def test_filter_reports_returns_correct_amount_of_reports(self):
        self.report4 = Report.objects.create(
            student = self.user,
            lab_group = self.labgroup,
            send_date = "2023-06-12",
            report_status = 0,
            comments = "",
        )
        self.report4.save()
        filtered_reports = filter_reports.filter_report(self.user.id)
        self.assertEqual(len(filtered_reports), 1)

    # Test for adding notes to a report

    def test_teacher_can_add_notes_to_a_report(self):
        notes = "this is a noteworthy thing"
        self.client.force_login(self.assistant)
        url = reverse("report_notes", args=[str(self.report1.id)])
        response = self.client.post(url, {"notes":notes})
        self.assertEqual(response.status_code, 302)

        self.report1.refresh_from_db()
        self.assertEqual(self.report1.notes, "this is a noteworthy thing")
    
    def test_student_cannot_add_notes_to_a_report(self):
        notes = "this is a noteworthy thing"
        self.client.force_login(self.user)
        url = reverse("report_notes", args=[str(self.report1.id)])
        response = self.client.post(url, {"notes":notes})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/my_labs")

        self.report1.refresh_from_db()
        self.assertEqual(self.report1.notes, "")
