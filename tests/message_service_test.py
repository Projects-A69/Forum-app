import unittest
from unittest.mock import patch
from services import messages_service

class TestMessagesService(unittest.TestCase):

    def setUp(self):
        self.sender_id = 1
        self.receiver_id = 2
        self.text = "Hello world"

    def test_create_messages(self):
        with patch('services.messages_service.insert_query') as mock_insert:
            mock_insert.return_value = 5
            result = messages_service.create_messages(self.sender_id, self.receiver_id, self.text)
            self.assertEqual(result["id"], 5)
            self.assertEqual(result["sender_id"], self.sender_id)
            self.assertEqual(result["receiver_id"], self.receiver_id)
            self.assertEqual(result["text"], self.text)

    def test_view_get_conversation(self):
        with patch('services.messages_service.read_query') as mock_read:
            mock_read.return_value = [(1, self.sender_id, self.text, "2024-01-01", self.receiver_id)]
            result = messages_service.view_get_conversation(self.sender_id, self.receiver_id)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["text"], self.text)
            self.assertEqual(result[0]["sender_id"], self.sender_id)

    def test_view_conversations(self):
        with patch('services.messages_service.read_query') as mock_read:
            mock_read.side_effect = [[(self.receiver_id,), (3,)], [(self.receiver_id, "Ivan")], [(3, "Ivan1")]]
            result = messages_service.view_conversations(self.sender_id)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["username"], "Ivan")
            self.assertEqual(result[1]["username"], "Ivan1")

    def test_view_get_conversation_empty(self):
        with patch('services.messages_service.read_query') as mock_read:
            mock_read.return_value = []
            result = messages_service.view_get_conversation(self.sender_id, self.receiver_id)
            self.assertEqual(result, [])





