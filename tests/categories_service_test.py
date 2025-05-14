import unittest
from unittest.mock import patch, Mock
from services import categories_service as service
from data.models import Category, CategoryCreate

class CategoriesServiceTest(unittest.TestCase):

    def setUp(self):
        self.user_id = 1

    @patch('services.categories_service.read_query')
    def test_get_by_id_returns_none_for_invalid_id(self, mock_query):
        mock_query.return_value = []
        result = service.get_by_id(1, user_id=self.user_id)
        self.assertIsNone(result)

    @patch('services.categories_service.read_query')
    def test_get_by_id_returns_403_if_private_and_no_access(self, mock_query):
        mock_query.side_effect = [
            [(1, "Private", "info", 1, "2023-01-01", 0)],  # category
            []  # topics
        ]
        with patch('services.categories_service.has_access', return_value=False):
            result = service.get_by_id(1, user_id=None)
            self.assertEqual(result, "no_write_access")

    @patch('services.categories_service.read_query')
    def test_create_category_successful(self, mock_read_query):
        category = CategoryCreate(name="Test", info="Test Info", is_private=False, date_created="2024-01-01", is_locked=False)

        with patch('services.categories_service.insert_query', return_value=1), \
             patch('services.categories_service.get_user_or_raise_401'), \
             patch('services.categories_service.read_query') as mock_read:

            mock_read.return_value = [(1, category.name, category.info, category.is_private, category.date_created, category.is_locked)]
            result = service.create_category(category, "token")

            self.assertIsInstance(result, Category)
            self.assertEqual(result.name, "Test")

    @patch('services.categories_service.read_query')
    @patch('services.categories_service.has_access', return_value=True)
    def test_get_by_id_returns_category_with_topics(self, mock_access, mock_read_query):
        mock_read_query.side_effect = [
            [(1, "Public", "info", 0, "2023-01-01", 0)],  # category
            [(1, "Title", "Text", 1, 1, 0, "2023-01-01", None)]  # topics
        ]

        result = service.get_by_id(1, user_id=1)
        self.assertIsInstance(result, Category)
        self.assertEqual(len(result.topics), 1)

    @patch('services.categories_service.update_query', return_value=1)
    @patch('services.categories_service.get_by_id')
    @patch('services.categories_service.get_user_or_raise_401')
    def test_lock_category_success(self, mock_auth, mock_get_by_id, mock_update):
        user = Mock(is_admin=True, id=1)
        mock_auth.return_value = user
        mock_get_by_id.return_value = Mock(is_locked=False)

        result = service.lock_category(1, "token")
        self.assertTrue(mock_update.called)
        self.assertEqual(mock_get_by_id.call_count, 2)
