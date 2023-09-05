from django.test import TestCase

class FirstTest(TestCase):
    def setUp(self):
        self.testApp = "IlmoWeb"

    def testing(self):
        self.assertEqual(self.testApp, "IlmoWeb")