from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User, Courses, Labs
from ilmoweb.logic import labs

class TestLabs(TestCase):
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
        self.lab1 = Labs.objects.create(
            course = self.course,
            name = "Kemian Labratyö-kurssi labra 1",
            description = "Labratyö-kurssin ensimmäinen labra",
            max_students = 20,
            is_visible = True
        )

        # invisible lab
        self.lab2 = Labs.objects.create(
            course = self.course,
            name = "Kemian Labratyö-kurssi labra 2",
            description = "Labratyö-kurssin toinen labra",
            max_students = 20,
            is_visible = False
        )
   
    # Tests for creating labs

    def test_post_request_creates_new_lab_and_redirects(self):
        self.client.force_login(self.superuser)

        data = {
            'lab_name': 'Lab',
            'description': 'Lab description',
            'max_students': str(5),
            'course_id': self.course.id
        }
        response = self.client.post(reverse('create_lab'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('created_labs'))

    def test_create_new_lab_when_max_students_is_0(self):
        lab_name = 'Awesome lab'
        description = 'This lab is awesome'
        max_students = 0
        course_id = self.course.id
        labs.create_new_lab(lab_name, description, max_students, course_id)

        new_lab = Labs.objects.get(name = lab_name)
        self.assertEqual(new_lab.max_students, 1)
    
    # Tests for activating labs

    def test_teacher_can_activate_lab(self):
        self.client.force_login(self.superuser)
        url = reverse("make_lab_visible", args=[str(self.lab2.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab2.refresh_from_db()
        self.assertEqual(self.lab2.is_visible, True)
    
    def test_teacher_can_deactivate_lab(self):
        self.client.force_login(self.superuser)
        url = reverse("make_lab_visible", args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.is_visible, False)
    
    def test_student_cannot_activate_lab(self):
        self.client.force_login(self.user)
        url = reverse("make_lab_visible", args=[str(self.lab2.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab2.refresh_from_db()
        self.assertEqual(self.lab2.is_visible, False)

    # Tests for deleting labs

    def test_teacher_can_delete_lab(self):
        self.client.force_login(self.superuser)
        url = reverse("delete_lab", args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.deleted, True)
    
    def test_student_cannot_delete_lab(self):
        self.client.force_login(self.user)
        url = reverse("delete_lab", args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.deleted, False)
