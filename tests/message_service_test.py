import unittest
from unittest.mock import patch
from data.models import Message, MessageCreate
from services.messages_service import create_message, view_conversation, view_conversations
import services.messages_service

TEST_SENDER_ID = 1
TEST_RECEIVER_ID = 2
TEST_TEXT = "Hello World"

def create_message(sender_id, receiver_id, text):
    return Message(
        sender_id = sender_id,
        receiver_id = receiver_id,
        text = text
    )

class TestMessageService(unittest.TestCase):

    def test_create_message(self):
        with patch('services.messages_service.create_message') as mock_create_message:
            services.messages_service.create_message(1,2, 'Hello World')
            mock_create_message.assert_called_with(1, 2, 'Hello World')

    def test_view_conversations(self):
        NotImplemented

    def test_view_conversation(self):
        NotImplemented



