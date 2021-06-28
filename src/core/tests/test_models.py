from django.test import TestCase
from django.contrib.auth import get_user_model


def create_mock_user(
    username='test',
    email='test@test.com',
    password='test123'
):
    """Create a new mock user"""
    get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password
    )


class UserModelTests(TestCase):
    """User model tests"""

    def setUp(self):
        self.mock_user = {
            'username': 'TestUser',
            'password': 'test123',
            'email': 'test@test.com',
        }

    def test_create_user_valid(self):
        """should create a new user to the database"""
        user = get_user_model().objects.create_user(
            **self.mock_user
        )

        self.assertEqual(user.username, self.mock_user['username'])
        self.assertTrue(user.check_password(self.mock_user['password']))
        self.assertEqual(user.email, self.mock_user['email'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_valid(self):
        """should create a new superuser to the database"""
        user = get_user_model().objects.create_superuser(
            **self.mock_user
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_uppercase_email(self):
        """should create a new user with normalized email"""
        mock_user = {
            **self.mock_user,
            'email': 'test@TeSt.COM'
        }
        user = get_user_model().objects.create_user(**mock_user)

        self.assertEqual(user.email, mock_user['email'].lower())

    def test_create_user_invalid_empty_username(self):
        """
        should fail to create a new user to the database due to empty usernam
        """
        with self.assertRaises(ValueError):
            invalid_mock_user = {
                **self.mock_user,
                'username': ''
            }
            get_user_model().objects.create_user(**invalid_mock_user)

    def test_create_user_invalid_no_username(self):
        """
        should fail to create a new user to the database
        due to missing username
        """
        with self.assertRaises(ValueError):
            invalid_mock_user = self.mock_user.copy()
            del invalid_mock_user['username']
            get_user_model().objects.create_user(**invalid_mock_user)

    def test_create_user_invalid_empty_email(self):
        """
        should fail to create a new user to the database due to empty email
        """
        with self.assertRaises(ValueError):
            invalid_mock_user = {
                **self.mock_user,
                'email': ''
            }
            get_user_model().objects.create_user(**invalid_mock_user)

    def test_create_user_invalid_no_email(self):
        """
        should fail to create a new user to the database due to missing email
        """
        with self.assertRaises(ValueError):
            invalid_mock_user = self.mock_user.copy()
            del invalid_mock_user['email']
            get_user_model().objects.create_user(**invalid_mock_user)
