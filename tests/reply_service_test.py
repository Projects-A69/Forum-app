import unittest
from unittest.mock import patch
from services import replies_service

class TestRepliesService(unittest.TestCase):

    def setUp(self):
        self.user_id = 1
        self.topic_id = 10
        self.replies_id = 5
        self.text = "This is a reply"
        self.vote_type = 1

    def test_create_reply_success(self):
        with patch('services.replies_service.read_query') as mock_read, \
             patch('services.replies_service.insert_query') as mock_insert:

            mock_read.return_value = [(1, False)]
            mock_insert.return_value = 12

            result = replies_service.create_replies(self.text, self.user_id, self.topic_id)
            self.assertEqual(result["id"], 12)
            self.assertEqual(result["text"], self.text)

    def test_create_reply_locked_topic(self):
        with patch('services.replies_service.read_query') as mock_read:
            mock_read.return_value = [(1, True)]
            result = replies_service.create_replies(self.text, self.user_id, self.topic_id)
            self.assertEqual(result, "topic is locked")

    def test_vote_reply_not_found(self):
        with patch('services.replies_service.read_query') as mock_read:
            mock_read.return_value = []

            result = replies_service.vote_replies(self.user_id, 999, self.vote_type)
            self.assertEqual(result, "Reply not found")

    def test_get_vote_reply(self):
        with patch('services.replies_service.read_query') as mock_read:
            mock_read.return_value = [(7, 2)]

            result = replies_service.get_vote_reply(self.replies_id)
            self.assertEqual(result, {"id": self.replies_id, "likes": 7, "dislikes": 2})
