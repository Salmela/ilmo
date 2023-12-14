from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase
from ilmoweb.models import User, Courses, Labs, LabGroups, Report, TeachersMessage

class FirstTest(TestCase):
    def setUp(self):
        self.testApp = "IlmoWeb"

    def test_mock_test(self):
        self.assertEqual(self.testApp, "IlmoWeb")

class TestModels(TestCase):
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

        # Teachers Message
        self.message = TeachersMessage.objects.create(
            message = "Hello students"
        )

        self.message.save()

    # Tests for User-model
    
    def test_user_is_created_with_correct_id(self):
        self.assertEqual(self.user.student_id, 100111222)

    def test_user_is_created_with_correct_username(self):
        self.assertEqual(self.user.username, "pvirtanen")

    def test_user_is_created_with_correct_password(self):
        self.assertTrue(check_password("virtanen", self.user.password))

    def test_user_is_created_with_correct_name(self):
        self.assertEqual(self.user.first_name, "Pekka")

    def test_user_is_created_with_correct_surname(self):
        self.assertEqual(self.user.last_name, "Virtanen")

    def test_user_is_created_with_correct_email(self):
        self.assertEqual(self.user.email, "pekka.virtanen@ilmoweb.fi")

    # Tests for Courses-model

    def test_course_is_created_with_correct_name(self):
        self.assertEqual(self.course.name, "Kemian Labratyö")

    def test_course_is_created_with_correct_description(self):
        self.assertEqual(self.course.description, "Kemian Labratyö-kurssi")

    def test_course_is_created_with_correct_labs_amount(self):
        self.assertEqual(self.course.labs_amount, 2)

    def test_course_is_created_with_correct_is_visible_value(self):
        self.assertFalse(self.course.is_visible)

    # Tests for Labs-model

    def test_lab_is_created_with_correct_name(self):
        self.assertEqual(self.lab.course, self.course)

    def test_lab_is_created_with_correct_name(self):
        self.assertEqual(self.lab.name, "Kemian Labratyö-kurssi labra 1")

    def test_lab_is_created_with_correct_description(self):
        self.assertEqual(self.lab.description, "Labratyö-kurssin ensimmäinen labra")

    def test_lab_is_created_with_correct_max_students_value(self):
        self.assertEqual(self.lab.max_students, 20)

    def test_lab_is_created_with_correct_is_visible_value(self):
        self.assertTrue(self.lab.is_visible)

    # Tests for LabGroups-model

    def test_lab_group_is_created_with_correct_lab(self):
        self.assertEqual(self.labgroup.lab, self.lab)

    def test_lab_group_is_created_with_correct_date(self):
        self.assertEqual(self.labgroup.date, "2023-06-01")

    def test_lab_group_is_created_with_correct_start_time(self):
        self.assertEqual(self.labgroup.start_time, "14:30")

    def test_lab_group_is_created_with_correct_end_time(self):
        self.assertEqual(self.labgroup.end_time, "16:30")

    def test_lab_group_is_created_with_correct_place(self):
        self.assertEqual(self.labgroup.place, "Chemicum")

    def test_lab_group_is_created_with_correct_is_visible_value(self):
        self.assertEqual(self.labgroup.status, 0)
    
    def test_lab_group_is_created_with_correct_assistant(self):
        self.assertEqual(self.labgroup.assistant, self.assistant)

    # Tests for Report-model
    def test_report_is_saved_to_db(self):
        self.all_reports = Report.objects.all()
        self.assertEqual(len(self.all_reports), 2)

    def test_saved_report_has_correct_fields(self):
        self.all_reports = Report.objects.all()
        self.assertEqual(self.all_reports[0].student, self.user)
        self.assertEqual(self.all_reports[0].lab_group, self.labgroup)
        self.assertEqual(self.all_reports[0].report_file, "raportti.pdf")
        self.assertEqual(self.all_reports[0].comments, "")
        self.assertEqual(self.all_reports[0].graded_by, None)

    # Tests for TeachersMessage-model
    def message_is_saved_to_db(self):
        get_message = TeachersMessage.objects.get(id=0)

        self.assertEqual(get_message, "Hello students")

