from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User

class TestLogin(TestCase):
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

        self.superuser = User.objects.create_superuser(
            username = "kemianope",
            password = "atomi123"
        )
        self.superuser.save()

        self.client=Client()

    # Tests for logging in and homepages

    def test_login_for_superuser(self):
        logged_in = self.client.login(username="kemianope", password="atomi123")
        self.assertTrue(logged_in)

    def test_login_with_wrong_password(self):
        logged_in = self.client.login(username="kemianope", password="chemicum")
        self.assertFalse(logged_in)

    def test_login_as_not_superuser(self):
        logged_in = self.client.login(username=self.user.username, password=self.user.password)
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
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        
        self.assertRedirects(response, reverse('open_labs'))
        
    def test_navigate_to_right_page_after_login_as_staff(self):
        self.client.force_login(self.assistant)
        response = self.client.get(reverse("home"))
        
        self.assertRedirects(response, reverse('created_labs'))

    def test_logged_out_user_gets_home_page(self):
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_student_can_not_get_to_created_labs(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('created_labs'))
        self.assertEqual(response.url, '/open_labs')
        self.assertEqual(response.status_code, 302)