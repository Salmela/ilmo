from django.contrib.auth.models import User as U
from django.test import TestCase, Client
from ilmoweb.models import User, Courses, Labs, LabGroups

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
            password = "virtanen",
            name = "Pekka",
            surname = "Virtanen",
            email = "pekka.virtanen@ilmoweb.fi"
        )

        self.course1 = Courses.objects.create(
            name = "Kemian Labratyö",
            description = "Kemian Labratyö-kurssi",
            labs_amount = 2,
            is_visible = False
        )

        self.lab1 = Labs.objects.create(
            course = self.course1,
            name = "Kemian Labratyö-kurssi labra 1",
            description = "Labratyö-kurssin ensimmäinen labra",
            max_students = 20,
            is_visible = True
        )

        self.labgroup1 = LabGroups.objects.create(
            lab = self.lab1,
            date = "2023-06-01",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            is_visible = False
        )
        # Creating a superuser for testing login
        self.superuser1 = U.objects.create_superuser(username='kemianope')
        self.superuser1.set_password('atomi123')
        self.superuser1.save()

        self.client=Client()

    # Tests for User-model
    def test_user_is_created_with_correct_id(self):
        self.assertEqual(self.user1.student_id, 100111222)

    def test_user_is_created_with_correct_username(self):
        self.assertEqual(self.user1.username, "pvirtanen")

    def test_user_is_created_with_correct_password(self):
        self.assertEqual(self.user1.password, "virtanen")

    def test_user_is_created_with_correct_name(self):
        self.assertEqual(self.user1.name, "Pekka")

    def test_user_is_created_with_correct_surname(self):
        self.assertEqual(self.user1.surname, "Virtanen")

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
        self.assertFalse(self.labgroup1.is_visible)

    # Tests for logging in as superuser
    def test_login_for_superuser(self):
        logged_in = self.client.login(username='kemianope', password='atomi123')

        self.assertTrue(logged_in)

    def test_login_with_wrong_password(self):
        logged_in = self.client.login(username='kemianope', password='chemicum')

        self.assertFalse(logged_in)

    def test_login_as_not_superuser(self):
        logged_in = self.client.login(username=self.user1.username, password=self.user1.password)

        self.assertFalse(logged_in)

#    def test_respond_with_correct_status_code(self):
#        response_get = self.client.get("/database_test/accounts/login/",
#                                    {'username':'kemianope', 'password':'atomi123'})
#        status_code_get = response_get.status_code
#        self.assertEqual(status_code_get, 200) # 200 OK
#
#        response_post = self.client.post("/database_test/accounts/login/",
#                                    {'username':'kemianope', 'password':'atomi123'})
#        status_code_post = response_post.status_code
#        self.assertEqual(status_code_post, 302) # 302 Found
