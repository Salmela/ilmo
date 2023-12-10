from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User

class TestPages(TestCase):
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

    # Tests for system page
    def test_only_super_user_gets_system_page(self):
        self.client.force_login(self.user)
        response_user = self.client.get(reverse('system'))
        self.assertEqual(response_user.status_code, 302)
        self.assertEqual(response_user.url, '/open_labs/')
        self.client.logout()

        self.client.force_login(self.assistant)
        response_staff = self.client.get(reverse('system'))
        self.assertEqual(response_staff.status_code, 302)
        self.assertEqual(response_staff.url, '/created_labs/')
        self.client.logout()

        self.client.force_login(self.superuser)
        response_superuser = self.client.get(reverse('system'))
        self.assertTemplateUsed(response_superuser, 'system.html')

    # Teachers Message
    def test_student_can_not_get_to_system_page_to_update_message(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('teachers_message'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/open_labs/')

    def test_assistant_can_not_get_to_system_page_to_update_message(self):
        self.client.force_login(self.assistant)
        response = self.client.get(reverse('teachers_message'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/created_labs/')

    def test_get_request_from_superuser_redirects_to_system(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('teachers_message'))
        self.assertRedirects(response, reverse('system'))
    
    # My labs
    def test_user_can_access_my_labs(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_labs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_labs.html")

    # Instuctions
    def test_intruction_page_is_rendered_with_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('instructions'))
        self.assertTemplateUsed(response, 'instructions.html')

    # Archive
    def test_student_can_not_access_archive(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('archive'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/open_labs')
        self.assertTemplateNotUsed(response, 'archive.html')

    def test_staff_can_access_archive(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('archive'))
        self.assertTemplateUsed(response, 'archive.html')
        self.assertEqual(response.status_code, 200)

    # Personal archive
    def test_student_can_not_access_personal_archive(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('personal_archive', args=[str(self.user.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/open_labs')
        self.assertTemplateNotUsed(response, 'personal_archive.html')
    
    def test_staff_can_access_personal_archive(self):
        self.client.force_login(self.assistant)
        response = self.client.get(reverse('personal_archive', args=[str(self.user.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal_archive.html')


    # Returned reports

    def test_student_can_not_access_returned_reports(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('returned_reports'))
        self.assertEqual(response.url, '/my_labs')
        self.assertEqual(response.status_code, 302)

    def test_staff_can_access_returned_reports(self):
        self.client.force_login(self.assistant)
        response = self.client.get(reverse('returned_reports'))
        self.assertTemplateUsed(response, 'returned_reports.html')

    # Create lab
    def test_student_can_not_get_create_lab_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_lab'))

        self.assertEqual(response.url, '/open_labs')
        self.assertEqual(response.status_code, 302)

    def test_staff_gets_correct_template_to_create_lab(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('create_lab'))
        self.assertTemplateUsed(response, 'create_lab.html')

    # Created Labs    
    def test_get_request_redirects_to_created_labs(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('labgroup_status'))
        self.assertRedirects(response, reverse('created_labs'))

    # Update multiple groups
    def test_students_get_request_redirects_to_open_labs(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('update_multiple_groups'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/open_labs')