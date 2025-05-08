import unittest
from unittest.mock import Mock, patch
from data.models import User, LoginData, RegisterData
from routers.api.users import login,register,promote_to_admin
import bcrypt

mock_users_service = Mock()

def fake_user(id=1, username="testuser", is_admin=False, password=None):
    mock_user = Mock(spec=User)
    mock_user.id = id
    mock_user.username = username
    mock_user.is_admin = is_admin
    if password:
        mock_user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return mock_user

class UsersRouterShould(unittest.TestCase):
    def setUp(self):
        mock_users_service.reset_mock()

    @patch('routers.api.users.users_service', mock_users_service)
    def test_login_with_valid_credentials_returns_token(self):
        test_password = "testpassword"
        test_user = fake_user(password=test_password)
        test_login = LoginData(username="testuser", password=test_password)
        
        mock_users_service.find_by_username.return_value = test_user
        mock_users_service.create_token.return_value = "test_token"
        
        result = login(test_login)
        
        self.assertIn("token", result)
        self.assertEqual(result["token"], "test_token")

    @patch('routers.api.users.users_service', mock_users_service)
    def test_login_with_invalid_credentials_returns_bad_request(self):
        mock_users_service.find_by_username.return_value = None
        test_login = LoginData(username="wrong", password="wrong")
        
        result = login(test_login)
        
        self.assertEqual(result.status_code, 400)
        self.assertIn("Invalid username or password", result.body.decode())

    @patch('routers.api.users.users_service', mock_users_service)
    def test_register_rejects_existing_username(self):
        test_user = fake_user()
        test_register = RegisterData(
            username="existing",
            telephone_number="1234567890",
            email="test@test.com",
            password="password"
        )
        mock_users_service.find_by_username.return_value = test_user
        
        result = register(test_register)
        
        self.assertEqual(result.status_code, 400)
        self.assertIn("already taken", result.body.decode())

    @patch('routers.api.users.users_service', mock_users_service)
    @patch('routers.api.users.get_user_or_raise_401')
    def test_promote_to_admin_requires_admin(self, mock_get_user):
        regular_user = fake_user(is_admin=False)
        mock_get_user.return_value = regular_user
        mock_users_service.make_user_admin.return_value = False
        
        result = promote_to_admin(2, "token")
        
        self.assertEqual(result.status_code, 400)
        self.assertIn("Only admins can promote", result.body.decode())