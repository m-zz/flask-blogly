from unittest import TestCase
from app import app
from models import Post

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

    def test_get_posts(self):
        with self.client as client:
            response = client.get("/posts/1")
            html = response.get_data(as_text=True)
            p = Post.query.get(1)
            self.assertEqual(p.user_id, 2)
            # escaped version in html, common in html
            self.assertIn("I&#39;m the first post!", html)
            
    def test_new_post(self):
        with self.client as client:
            response = client.post("/users/1/posts/new",
                data={'p_title':'Disneyland', 'p_content':'Welcome to Disneyland!'},
                follow_redirects=True )
            html = response.get_data(as_text=True)
            self.assertIn('Disneyland', html)

    def test_edit_post(self):
        with self.client as client:
            response = client.post("/posts/2/edit",
                data={'p_title':'Disneyworld!', 'p_content':'Florida does it better!!!'},
                follow_redirects=True )
            html = response.get_data(as_text=True)
            self.assertIn('Disneyworld!', html)

# delete test