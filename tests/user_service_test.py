import unittest
from unittest.mock import Mock, patch
from jose import jwt
from data.models import User
from services.users_service import find_by_username,create_token,is_authenticated,make_user_admin


class UsersServiceShould(unittest.TestCase):
    def setUp(self):
        self.mock_read_query = Mock()
        self.mock_insert_query = Mock()
        self.mock_update_query = Mock()
        
        self.patchers = [
            patch('services.users_service.read_query', self.mock_read_query),
            patch('services.users_service.insert_query', self.mock_insert_query),
            patch('services.users_service.update_query', self.mock_update_query)
        ]
        
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()

    def test_find_by_username_returns_user(self):
        test_data = [(1, "testuser", "123", "test@test.com", False, "hashed", "2023-01-01")]
        self.mock_read_query.return_value = test_data
        
        result = find_by_username("testuser")
        
        self.assertEqual(result.username, "testuser")
        self.assertEqual(result.id, 1)

    def test_create_token_generates_valid_jwt(self):
        test_user = User(id=1,
            username="testuser",
            telephone_number="1234567890",
            email="test@test.com",
            password="hashed",
            is_admin=False,
            date_registration="2023-01-01")
        
        token = create_token(test_user)
        payload = jwt.decode(token, "123", algorithms=["HS256"])
        
        self.assertEqual(payload["username"], "testuser")
        self.assertEqual(payload["user_id"], 1)

    def test_is_authenticated_validates_token(self):
        test_user = User(id=1,
            username="testuser",
            telephone_number="1234567890",
            email="test@test.com",
            password="hashed",
            is_admin=False,
            date_registration="2023-01-01")
        valid_token = create_token(test_user)
        
        self.mock_read_query.return_value = [(1, "testuser", "1234567890", "test@test.com", False, "hashed", "2023-01-01")]
        
        result = is_authenticated(valid_token)
        self.assertTrue(result)


    def test_make_user_admin_requires_admin(self):
        regular_user = User(id=1,
            username="regular",
            telephone_number="1234567890",
            email="regular@test.com",
            password="password",
            is_admin=False,
            date_registration="2023-01-01")
        
        admin_user = User(id=2,
            username="admin",
            telephone_number="9876543210",
            email="admin@test.com",
            password="adminpass",
            is_admin=True,
            date_registration="2023-01-01")
        
        result = make_user_admin(regular_user, 2)
        self.assertFalse(result)
        
        self.mock_read_query.return_value = [(2,)]
        result = make_user_admin(admin_user, 2)
        self.assertTrue(result)
        
        self.mock_read_query.return_value = []
        result = make_user_admin(admin_user, 999)
        self.assertIsNone(result)