import unittest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from data.models import ReplyCreate, RepliesHasUsers
from routers.api.replies import create_reply, vote_reply

class ReplyRouterTest(unittest.TestCase):

    def setUp(self):
        self.user = Mock()
        self.user.id = 1
        self.token = "token"
        self.reply = ReplyCreate(user_id=1, topic_id=10, text="Good")
        self.vote = RepliesHasUsers(users_id=1, replies_id=5, vote_type=1)

    def test_create_reply(self):
        with patch('routers.api.replies.get_user_or_raise_401') as mock_user, \
            patch('routers.api.replies.get_by_id') as mock_get_topic, \
            patch('routers.api.replies.has_access') as mock_access, \
            patch('routers.api.replies.create_replies') as mock_create:
            mock_user.return_value = self.user
            mock_get_topic.return_value = Mock(category_id=1, is_locked = False)
            mock_access.return_value = True
            mock_create.return_value = {"text": self.reply.text}
            result = create_reply(reply = self.reply, x_token = self.token)

            self.assertEqual(result["text"], self.reply.text)

    def test_create_reply_topic_locked(self):
        with patch('routers.api.replies.get_user_or_raise_401') as mock_user, \
                patch('routers.api.replies.get_by_id') as mock_get_topic, \
                patch('routers.api.replies.has_access') as mock_access, \
                patch('routers.api.replies.create_replies') as mock_create:
            mock_user.return_value = self.user
            mock_get_topic.return_value = Mock(category_id=1, is_locked=False)
            mock_access.return_value = True
            mock_create.return_value = "topic is locked"
            with self.assertRaises(HTTPException) as context:
                create_reply(reply = self.reply, x_token = self.token)
            self.assertEqual(context.exception.status_code, 404)
            self.assertEqual(context.exception.detail, "Topic is locked")

    def test_create_reply_no_access(self):
        with patch('routers.api.replies.get_user_or_raise_401') as mock_user, \
                patch('routers.api.replies.get_by_id') as mock_get_topic, \
                patch('routers.api.replies.has_access') as mock_access:
            mock_user.return_value = self.user
            mock_get_topic.return_value = Mock(category_id=1, is_locked=False)
            mock_access.return_value = False
            with self.assertRaises(HTTPException) as context:
                create_reply(reply = self.reply, x_token = self.token)
            self.assertEqual(context.exception.status_code, 403)

    def test_create_reply_no_topic(self):
        with patch('routers.api.replies.get_user_or_raise_401') as mock_user, \
                patch('routers.api.replies.get_by_id') as mock_get_topic:
            mock_user.return_value = self.user
            mock_get_topic.return_value = None
            with self.assertRaises(HTTPException) as context:
                create_reply(reply = self.reply, x_token = self.token)
            self.assertEqual(context.exception.status_code, 404)

    def test_vote_reply(self):
        with patch('routers.api.replies.get_user_or_raise_401') as mock_user, \
            patch('routers.api.replies.vote_replies') as mock_vote_reply:
            mock_user.return_value = self.user
            mock_vote_reply.return_value = {"likes": 1, "dislikes": 5}
            result = vote_reply(vote_reply = self.vote, x_token = self.token)
            self.assertEqual(result["likes"], 1)
            self.assertEqual(result["dislikes"], 5)

    def test_vote_reply_no_found(self):
        with patch('routers.api.replies.get_user_or_raise_401') as mock_user, \
                patch('routers.api.replies.vote_replies') as mock_vote_reply:
            mock_user.return_value = self.user
            mock_vote_reply.return_value = "Reply not found"
            with self.assertRaises(HTTPException) as context:
                vote_reply(vote_reply = self.vote, x_token = self.token)
            self.assertEqual(context.exception.status_code, 404)

