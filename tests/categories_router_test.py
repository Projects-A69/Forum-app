import unittest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from data.models import CategoryCreate, Category
from routers.api.categories import view_category_router, create_categories_router, lock_category_router, view_categories_router

mock_service = Mock()
mock_auth = Mock()

def fake_user():
    user = Mock()
    user.id = 1
    user.is_admin = True
    return user

class CategoriesRouterTest(unittest.TestCase):

    def setUp(self):
        self.token = "valid_token"
        self.user = fake_user()
        mock_service.reset_mock()

    @patch('routers.api.categories.get_by_id', mock_service.get_by_id)
    def test_view_category_returns_category(self):
        category = Mock(spec=Category)
        mock_service.get_by_id.return_value = category

        result = view_category_router(id=1, user_id=1)
        self.assertEqual(result, category)

    @patch('routers.api.categories.get_by_id', mock_service.get_by_id)
    def test_view_category_returns_403_if_no_access(self):
        mock_service.get_by_id.return_value = "no_write_access"

        with self.assertRaises(HTTPException) as context:
            view_category_router(id=1, user_id=1)

        self.assertEqual(context.exception.status_code, 403)

    @patch('routers.api.categories.get_by_id', mock_service.get_by_id)
    def test_view_category_returns_404_if_not_found(self):
        mock_service.get_by_id.return_value = None

        with self.assertRaises(HTTPException) as context:
            view_category_router(id=1, user_id=1)

        self.assertEqual(context.exception.status_code, 404)

    @patch('routers.api.categories.create_category', mock_service.create_category)
    @patch('routers.api.categories.get_user_or_raise_401', mock_auth.get_user_or_raise_401)
    def test_create_category_succeeds(self):
        category_create = CategoryCreate(name="Test", info="Info", is_private=False, date_created="2024-01-01", is_locked=False)
        mock_auth.get_user_or_raise_401.return_value = self.user
        mock_service.create_category.return_value = "ok"

        result = create_categories_router(category_create, self.token)
        self.assertEqual(result, "ok")

    @patch('routers.api.categories.lock_category', mock_service.lock_category)
    @patch('routers.api.categories.get_user_or_raise_401', mock_auth.get_user_or_raise_401)
    def test_lock_category_succeeds(self):
        mock_auth.get_user_or_raise_401.return_value = self.user
        mock_service.lock_category.return_value = "locked"

        result = lock_category_router(id=1, x_token=self.token)
        self.assertEqual(result, "locked")

    @patch('routers.api.categories.get_all_categories', mock_service.get_all_categories)
    def test_view_categories_returns_list(self):
        mock_service.get_all_categories.return_value = ["cat1", "cat2"]

        result = view_categories_router()
        self.assertEqual(len(result), 2)
