from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from .models import Topic, Question, Questionoptions, User
from .views import GenerateQuestions, GenerateMore

class MockedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = MagicMock(spec=User)
        self.user.userid = 1
        self.topic = MagicMock(spec=Topic)
        self.topic.topicid = 1
        self.topic.title = "Test Topic"
        self.topic.data = "Test data for generating questions."

class TopicAPITests(MockedTestCase):
    @patch('django.db.connection')
    @patch('api.views.Topic.objects.all')
    def test_get_all_topics(self, mock_all, mock_connection):
        mock_all.return_value = [self.topic]
        response = self.client.get(reverse('Topics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['topics']), 1)

    @patch('django.db.connection')
    @patch('api.views.Topic.objects.create')
    @patch('api.views.GenerateQuestions')
    def test_create_topic(self, mock_generate, mock_create, mock_connection):
        mock_create.return_value = self.topic
        mock_generate.return_value = {"Question 1": {"Option 1": True, "Option 2": False}}
        payload = {
            "title": "New Topic",
            "maxquestions": 5,
            "userid": self.user.userid,
            "data": "New topic data"
        }
        response = self.client.post(reverse('Topics'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class QuestionAPITests(MockedTestCase):
    @patch('django.db.connection')
    @patch('api.views.Question.objects.get')
    def test_get_question_detail(self, mock_get, mock_connection):
        question = MagicMock(spec=Question)
        question.questionid = 1
        question.question = "Test question?"
        mock_get.return_value = question
        response = self.client.get(reverse('QuestionDetail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GenerateQuestionsTests(MockedTestCase):
    @patch('django.db.connection')
    @patch('api.views.Topic.objects.get')
    @patch('api.views.GenerateMore')
    @patch('api.views.Question.objects.create')
    @patch('api.views.Questionoptions.objects.create')
    def test_generate_questions(self, mock_options_create, mock_question_create, mock_generate_more, mock_get, mock_connection):
        mock_get.return_value = self.topic
        mock_generate_more.return_value = {"Question 1": {"Option 1": True, "Option 2": False}}
        mock_question_create.return_value = MagicMock(spec=Question)
        mock_options_create.return_value = MagicMock(spec=Questionoptions)

        response = self.client.post(reverse('Generate', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_generate_more.assert_called_once()
        mock_question_create.assert_called_once()
        self.assertEqual(mock_options_create.call_count, 2)  # Two options created