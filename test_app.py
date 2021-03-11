from unittest import TestCase
from app import app

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

class BloglyTestCase(TestCase):
    
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """tests success code and correct page of homepage"""
        with self.client as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("<ul>" , html)

    def test_new_user_page(self):
        with self.client as client:
            response = client.get("/users/new")
            html = response.get_data(as_text=True)
            self.assertIn('Create a User', html)

    def test_create_user(self):
        with self.client as client:
            response = client.post("/users/new",
                data={'f_name':'Tom', 'l_name':'Brady', 'img_url': ''},
                follow_redirects=True )
            html = response.get_data(as_text=True)
            self.assertIn('Tom Brady', html)

    def test_edit_user(self):
        with self.client as client:
            response = client.get("/users/1/edit")
            html = response.get_data(as_text=True)
            self.assertIn('Edit a User', html)

    def test_successful_edit(self):
        with self.client as client:
            response = client.post("/users/1/edit",
                data={'f_name':'Elon', 'l_name':'Musk', 'img_url': ''},
                follow_redirects=True )
            html = response.get_data(as_text=True)
            self.assertIn('Elon Musk', html)
