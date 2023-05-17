from django.test import TestCase

# Create your tests here.
class SmapleTest(TestCase):
    def test_sample(self):
        a = 1 + 1
        self.assertEqual(a, 2)