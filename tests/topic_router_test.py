import unittest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from data.models import Topic, TopicCreate
from routers.api.topics import get_topics,get_topic_by_id,create_topic_router,lock_topic_route,choose_best_reply_route


mock_topics_service = Mock()
mock_auth_service = Mock()

def fake_topic(id=1, title="Test Topic", user_id=1, replies=None):
    if replies is None:
        replies = []
    mock_topic = Mock(spec=Topic)
    mock_topic.id = id
    mock_topic.title = title
    mock_topic.user_id = user_id
    mock_topic.replies = replies
    mock_topic.date_created = "2023-01-01"
    return mock_topic

class TopicsRouterShould(unittest.TestCase):
    def setUp(self):
        mock_topics_service.reset_mock()
        mock_auth_service.reset_mock()

    @patch('routers.api.topics.get_all', mock_topics_service.get_all)
    def test_get_topics_returns_list_of_topics(self):
        test_topic = fake_topic()
        mock_topics_service.get_all.return_value = [test_topic]
        
        result = get_topics()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, test_topic.title)

    @patch('routers.api.topics.get_all', mock_topics_service.get_all)
    def test_get_topics_with_invalid_sort_raises_exception(self):
        with self.assertRaises(HTTPException) as context:
            get_topics(sort="invalid")
            
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Invalid sort value", context.exception.detail)

    @patch('routers.api.topics.get_by_id', mock_topics_service.get_by_id)
    def test_get_topic_by_id_returns_not_found_when_no_topic(self):
        mock_topics_service.get_by_id.return_value = None
        
        with self.assertRaises(HTTPException) as context:
            get_topic_by_id(1)
            
        self.assertEqual(context.exception.status_code, 404)

    @patch('routers.api.topics.create_topic', mock_topics_service.create_topic)
    @patch('routers.api.topics.get_user_or_raise_401', mock_auth_service.get_user_or_raise_401)
    def test_create_topic_router_handles_category_not_found(self):
        test_user = Mock(id=1)
        test_topic = TopicCreate(title="Test", text="Test", category_id=1)
        mock_auth_service.get_user_or_raise_401.return_value = test_user
        mock_topics_service.create_topic.return_value = "category_not_found"
        
        with self.assertRaises(HTTPException) as context:
            create_topic_router(test_topic, "token")
            
        self.assertEqual(context.exception.status_code, 404)

    @patch('routers.api.topics.lock_topic', mock_topics_service.lock_topic)
    @patch('routers.api.topics.get_user_or_raise_401', mock_auth_service.get_user_or_raise_401)
    def test_lock_topic_route_requires_admin(self):
        test_user = Mock(is_admin=False)
        mock_auth_service.get_user_or_raise_401.return_value = test_user
        
        with self.assertRaises(HTTPException) as context:
            lock_topic_route(1, "token")
            
        self.assertEqual(context.exception.status_code, 403)

    @patch('routers.api.topics.choose_best_reply', mock_topics_service.choose_best_reply)
    @patch('routers.api.topics.get_user_or_raise_401', mock_auth_service.get_user_or_raise_401)
    @patch('routers.api.topics.get_by_id', mock_topics_service.get_by_id)
    def test_choose_best_reply_validates_author(self):
        test_user = Mock(id=2)
        test_topic = fake_topic(user_id=1)
        mock_auth_service.get_user_or_raise_401.return_value = test_user
        mock_topics_service.choose_best_reply.return_value = "not_author"
        mock_topics_service.get_by_id.return_value = test_topic
        
        with self.assertRaises(HTTPException) as context:
            choose_best_reply_route(1, 1, "token")
            
        self.assertEqual(context.exception.status_code, 403)