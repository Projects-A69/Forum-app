import unittest
from routers.api.topics import get_topic_by_id
from routers.api import replies as reply_router
from unittest.mock import Mock, patch
from data.models import Reply, ReplyCreate
from services.topics_service import topic_service


def fake_topic():
    topic = Mock()
    topic.id = 1
    topic.title = 'Test'
    topic.category_id = 1
    return topic

def fake_replies():
    user = Mock()
    user.id = 1
    return user

class TestReplyRouter(unittest.TestCase):
    def setUp(self):
        self.mock_topic_service = Mock(spec='services.topics_service')
        self.mock_reply_service = Mock(spec='services.reply_service')
        reply_router.topics_service = self.mock_topic_service
        reply_router.replies_service = self.mock_reply_service

        self.topic = fake_topic()
        self.replies = fake_replies()
        self.token = "token"

    def test_create_replies(self):
        reply = ReplyCreate(user_id = 1, topic_id = 1, text = "Hello World")
        with patch('routers.replies.get_user_or_raise_401') as mock_get_user:
            mock_get_user.return_value = self.replies
            self.mock_topic_service.get_by_id.return_value = self.topic
            self.mock_reply_service.create.return_value = None
            result = reply_router.create_replies(reply = reply, x_token = self.token)
            self.assertIsNone(result)

    def test_inccorect_create_replies(self):
        NotImplemented

    def test_vote_replies(self):
        NotImplemented

    def test_incorect_vote_replies(self):
        NotImplemented