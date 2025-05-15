import unittest
from unittest.mock import Mock, patch
from data.models import TopicCreate
from services.topics_service import get_all,get_by_id,create_topic,lock_topic,choose_best_reply

class TopicsServiceShould(unittest.TestCase):
    def setUp(self):
        self.mock_read_query = Mock()
        self.mock_insert_query = Mock()
        self.mock_has_access = Mock(return_value=True)
        
        self.patchers = [patch('services.topics_service.read_query', self.mock_read_query),
            patch('services.topics_service.insert_query', self.mock_insert_query),
            patch('services.topics_service.has_access', self.mock_has_access)]
        
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()

    def test_get_all_returns_sorted_topics(self):
        test_data = [[(1, "Topic 1", "Content", 1, 1, None, "2023-01-02"),
            (2, "Topic 2", "Content", 1, 1, None, "2023-01-01")],
            [],[]]
        
        self.mock_read_query.side_effect = test_data
        result = get_all(sort='asc')
        self.assertEqual(result[0].id, 2)
        
        self.mock_read_query.side_effect = test_data
        result = get_all(sort='desc')
        self.assertEqual(result[0].id, 1)

    def test_get_by_id_returns_topic_with_replies(self):
        created_date = "2023-01-01 00:00:00"
        updated_date = "2023-01-02 00:00:00"
        
        self.mock_read_query.side_effect = [[(1, "Topic 1", "Content", 1, 1, None)],
            [(1, "Reply text", created_date, updated_date, 2, 1)]]
        
        result = get_by_id(1)
        
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Topic 1")
        self.assertEqual(len(result.replies), 1)
        reply = result.replies[0]
        self.assertEqual(reply.id, 1)
        self.assertEqual(reply.text, "Reply text")

    def test_choose_best_reply_validates_conditions(self):
        test_topic = Mock()
        test_topic.user_id = 1
        with patch('services.topics_service.get_by_id', return_value=test_topic):
            self.mock_read_query.return_value = [(1,)]
            result = choose_best_reply(1, 1, 2)
            self.assertEqual(result, "not_author")
            
            self.mock_read_query.return_value = []
            result = choose_best_reply(1, 1, 1)
            self.assertEqual(result, "reply_not_found")