import os
import unittest
import tempfile
import uuid
from app import app, get_db_connection

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True

        # Setup an in-memory SQLite database for testing
        app.config['DATABASE'] = 'sqlite:///:memory:'

        # Initialize the in-memory database
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()

        with app.app_context():
            conn = get_db_connection()
            conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)')
            conn.commit()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_register_success(self):
        unique_username = f"testuser_{uuid.uuid4()}"
        response = self.app.post('/register', data={'username': unique_username, 'password': 'testpass'}, follow_redirects=True)
        
        # Check if the user is redirected to the success page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User created successfully', response.data)

        # Check the database
        with app.app_context():
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE username = ?', (unique_username,))
            user = cur.fetchone()
            self.assertIsNotNone(user)
            self.assertEqual(user['username'], unique_username)

    def test_register_existing_username(self):
        existing_username = "existing_user"
        response = self.app.post('/register', data={'username': existing_username, 'password': 'testpass'}, follow_redirects=True)
        
        # Check if the user receives an error message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists', response.data)

    def test_access_test_page(self):
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Test page")

if __name__ == '__main__':
    unittest.main()
