from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase, Client
from ilmoweb.models import User, Courses, Labs, LabGroups
from ilmoweb.logic import labgroups

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

        # empty labgroup
        self.labgroup1 = LabGroups.objects.create(
            lab = self.lab1,
            date = "2023-06-01",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            status = False
        )

        # nonempty labgroup
        self.labgroup2 = LabGroups.objects.create(
            lab = self.lab1,
            date = "2023-06-02",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            status = False,
            signed_up_students = 1
        )
        # Creating a superuser for testing login
        self.superuser1 = User.objects.create_superuser(
            username = 'kemianope',
            password = 'atomi123'
        )
        self.superuser1.save()

        self.client=Client()

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

    def test_respond_with_correct_status_code_login(self):
        response_get = self.client.get("/accounts/login/",
                                    {'username':'kemianope', 'password':'atomi123'})
        status_code_get = response_get.status_code
        self.assertEqual(status_code_get, 200) # 200 OK

        response_post = self.client.post("/accounts/login/",
                                    {'username':'kemianope', 'password':'atomi123'})
        status_code_post = response_post.status_code
        self.assertEqual(status_code_post, 302) # 302 Found

    def test_logout(self):
        logged_in = self.client.login(username='kemianope', password='atomi123')
        logged_in = self.client.logout()
        self.assertFalse(logged_in)

    def test_respond_with_correct_status_code_logout(self):
        response_get = self.client.get("/accounts/logout/",
                                    {'username':'kemianope', 'password':'atomi123'})
        status_code_get = response_get.status_code
        self.assertEqual(status_code_get, 302) # 302 Found

    # Tests for labgroup enrollment

    def test_student_can_enroll_to_labgroup(self):
        self.client.login(username=self.user1.username, password=self.user1.password)
        data = {
            'user_id': self.user1.id,
            'group_id': self.labgroup1.id
        }
        response_post = self.client.post('/open_labs/', data, 'application/json')
        self.assertEqual(response_post.status_code, 200)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.signed_up_students, 1)
    
    def test_student_cannot_enroll_twice_to_same_labgroup(self):
        self.client.login(username=self.user1.username, password=self.user1.password)
        data = {
            'user_id': self.user1.id,
            'group_id': self.labgroup1.id
        }
        self.client.post('/open_labs/', data, 'application/json')
        with self.assertRaises(ValueError):
            self.client.post('/open_labs/', data, 'application/json')
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.signed_up_students, 1)
    
    def test_teacher_can_confirm_nonempty_labgroup(self):
        self.client.login(username=self.superuser1.username, password=self.superuser1.password)
        response_post = self.client.post('/open_labs/confirm/', self.labgroup2.id, 'application/json')
        self.assertEqual(response_post.status_code, 302)
        self.labgroup2.refresh_from_db()
        self.assertEqual(self.labgroup2.status, 2)
    
    def test_teacher_cannot_confirm_empty_labgroup(self):
        self.client.login(username=self.superuser1.username, password=self.superuser1.password)
        response_post = self.client.post('/open_labs/confirm/', self.labgroup1.id, 'application/json')
        self.assertEqual(response_post.status_code, 400)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.status, False)
    
    # Tests for creating labgroups

    def test_start_end_times_8_to_12(self):
        lab = self.lab1
        date = '2023-10-13'
        time = '8-12'
        place = 'B105'

        labgroups.create(lab, date, time, place)

        group = LabGroups.objects.get(lab=lab, date=date, place=place)

        self.assertEqual(group.start_time.hour, 8)
        self.assertEqual(group.end_time.hour, 12)

    def test_start_end_times_12_to_16(self):
        lab = self.lab1
        date = '2023-10-13'
        time = '12-16'
        place = 'B105'

        labgroups.create(lab, date, time, place)

        group = LabGroups.objects.get(lab=lab, date=date, place=place)

        self.assertEqual(group.start_time.hour, 12)
        self.assertEqual(group.end_time.hour, 16)

