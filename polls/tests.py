from django.test import TestCase
from django.utils import timezone
from .models import Question
import datetime
from django.urls import reverse

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_published_recent_with_future_date(self):
        t = timezone.now() + datetime.timedelta(days=30)
        q = Question(pub_date=t.date())
        self.assertIs(q.was_published_recently(), False)
    
    def test_published_recent_with_old_date(self):
        t = timezone.now() - datetime.timedelta(days=2, seconds=1)
        q = Question(pub_date=t.date())
        self.assertIs(q.was_published_recently(), False)

def create_question(question_text, days):
    """ create a question with the question text and days arguments. days negative for a time in the past"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertIs(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_question(self):
        """ this is to ensure that past questions are displayed as expected"""
        question = create_question(question_text="A past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions"],
            [question]
        )

    def test_future_question(self):
        create_question(question_text="a future test", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_and_future_questions(self):
        past = create_question(question_text="past", days=-30)
        create_question(question_text="future", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [past])

    def test_multiple_past_question(self):
        question1 = create_question(question_text="question1", days=-30)
        question2 = create_question(question_text="question2", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question1, question2])