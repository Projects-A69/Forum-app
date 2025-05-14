import unittest
from http.client import HTTPException
from unittest.mock import Mock, patch
from data.models import Message, MessageCreate
from routers.api.messages import messages_router, create_message, view_conversation
from common.responses import NotFound, Unauthorized

mock_message_service = Mock(spec='services.message_service')
messages_router.message_service = mock_message_service

def fake_user():
    user = Mock()
    user.id = 1
    return user

class MessageRouterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.user = fake_user()
        self.token = "token"

    def test_return_correctMessage(self):
        message = MessageCreate(sender_id=1, receiver_id=1, text='Hello World')
        with patch('routers.messages.get_user_or_raise_401') as mock_get_user:
            mock_get_user.return_value = self.user

            result = create_message(message=message, x_token=self.token)

            self.assertIsNone(result)

    def test_return_incorrect_sender(self):
        message = MessageCreate(sender_id=9999, receiver_id=1, text='Hello World')
        with patch('routers.messages.get_user_or_raise_401') as mock_get_user:
            mock_get_user.return_value = self.user
            with self.assertRaises(HTTPException) as context:
                create_message(message=message, x_token=self.token)
            self.assertEqual(context.exception.status_code, 401)
            self.assertEqual(context.exception.detail,'Sender ID not found')


    def test_return_Conversation(self):
        with patch('routers.messages.get_user_or_raise_401') as mock_get_user:
            mock_get_user.return_value = self.user

            with patch('routers.messages.view_conversation') as mock_view_conversation:
                mock_view_conversation.return_value = "Hello World"
                result = view_conversation(sender_id=1, receiver_id=1, x_token=self.token)

                self.assertEqual(result, 'Hello World')
