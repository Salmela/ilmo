from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User, TeachersMessage
from ilmoweb.logic import teachermessage

class TestTeachersMessage(TestCase):
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

        self.superuser = User.objects.create_superuser(
            username = "kemianope",
            password = "atomi123"
        )
        self.superuser.save()

        self.client=Client()

        self.message = TeachersMessage.objects.create(
            message = "Hello students"
        )

        self.message.save()

    def test_messages_are_updated(self):

        self.client.force_login(self.superuser)

        new_message="Hi students"
        self.client.post("/teachers_message/", {"message":new_message})

        self.message.refresh_from_db()

        self.assertEqual(self.message.message, "Hi students")

    def test_student_can_not_send_message(self):
        self.client.force_login(self.user)
        new_message = "Hello from a fellow student"
        response = self.client.post("/teachers_message/", {"message": new_message})
        self.assertEqual(response.status_code, 302)

        message = self.message.message
        self.assertNotEqual(message, new_message)

    def test_update_function_in_teachermessage(self):
        new_message = 'Goodbye students'
        teachermessage.update(new_message)

        message = TeachersMessage.objects.get(message = new_message)
        self.assertEqual(message.message, new_message)