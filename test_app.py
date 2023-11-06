import unittest
from app import app
from flask import request, session

class TestApp(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_summary(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)


    def test_spendings_get(self):
        response = self.client.get("/spendings")
        self.assertEqual(response.status_code, 302)


    def test_budgeting_get(self):
        response = self.client.get("/budgeting")
        self.assertEqual(response.status_code, 302)


    def test_savings_get(self):
        response = self.client.get("/savings")
        self.assertEqual(response.status_code, 302)


    def test_showspendings_get(self):
        response = self.client.get("/showspendings")
        self.assertEqual(response.status_code, 302)

    #def test_login(self):
    #    with self.client:
    #        current_user = {"username": "ABC", "password": '3rjirAekjweoA2039#$opf'}
    #        response = self.client.post('login', { "username": 'ABC', "password": '3rjirAekjweoA2039#$opf' })
#
    #    self.assertEquals(current_user["username"], 'ABC')

    #def test_foo_with_client(self):
    #    rv = self.client.get('/hello?q=paramfoo')
    #    self.assertEqual(request.args['q'], 'paramFoo')    # Assertion succeeds
    #    # Do a POST request with valid credentials to login
    #    self.client.post('/login', data={'username': 'a', 'password': 'b'})
    #    # Our flask app sets userId in session on a successful login
    #    self.assertIn('userId', session) # Assertion succeeds

if __name__ == "__main__":
    unittest.main()