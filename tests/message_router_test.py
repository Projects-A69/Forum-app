import unittest
from fastapi import HTTPException
from unittest.mock import Mock, patch
from data.models import Message, MessageCreate
from routers.api.messages import messages_router, create_message, view_conversation
from common.responses import NotFound, Unauthorized

class MessageRouterTest(unittest.TestCase):

    def setUp(self):
        self.user = Mock()
        self.user.id = 1
        self.token = "token"
        self.message = MessageCreate(sender_id=1, receiver_id=2, text="Hello!")

    def test_create_message_success(self):
        with patch('routers.api.messages.get_user_or_raise_401') as mock_user, \
            patch('routers.api.messages.create_messages') as mock_create:
            mock_user.return_value = self.user
            mock_create.return_value = {"message": "Hello!", "receiver_id": 2}
            result = create_message(message=self.message, x_token=self.token)
            self.assertEqual(result["message"], "Hello!")

    def test_return_incorrect_sender(self):
        message = MessageCreate(sender_id=9999, receiver_id=55555, text='Hello World')
        with patch('routers.api.messages.get_user_or_raise_401') as mock_user, \
                patch('routers.api.messages.create_messages') as mock_create:
            mock_user.return_value = self.user
            with self.assertRaises(HTTPException) as context:
                create_message(message=message, x_token=self.token)
            self.assertEqual(context.exception.status_code, 401)
            self.assertEqual(context.exception.detail,'User ID does not exist')


    def test_return_conversation(self):
        with patch('routers.api.messages.get_user_or_raise_401') as mock_get_user, \
            patch('routers.api.messages.view_get_conversation') as mock_view_conversation:
                mock_get_user.return_value = self.user
                mock_view_conversation.return_value = [{"text": "Hello"}]
                result = view_conversation(sender_id=1, receiver_id=1, x_token=self.token)

                self.assertEqual(result[0]["text"], 'Hello')

    def test_return_unauthorized_conversation(self):
        with patch('routers.api.messages.get_user_or_raise_401') as mock_user:
            mock_user.return_value = self.user

            with self.assertRaises(HTTPException) as context:
                view_conversation(sender_id=10000, receiver_id=1000000, x_token=self.token)

            self.assertEqual(context.exception.status_code, 401)
            self.assertEqual(context.exception.detail,'Access denied')

    def test_return_all_conversation(self):
        with patch('routers.api.messages.get_user_or_raise_401') as mock_user, \
            patch('router.api.messages.view_conversation') as mock_view_conversation:
            mock_user.return_value = self.user
            mock_view_conversation = [{"id": 2, "username": "Ivan"}]
            result = view_conversation(x_token=self.token)
            self.assertEqual(result[0]["username"], 'Ivan')

