import datetime
from django.test import TestCase

from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_future_question(self):
        future_question = Question(pub_date = timezone.now() + datetime.timedelta(days=30))
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_old_question(self):
        old_question = Question(timezone.now() - datetime.timedelta(days=1,seconds=1))
        self.assertIs(old_question.was_published_recently(), False)

def create_question(question_text,days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date = time) #creates a new object saved in database when created

class IndexViewTests(TestCase):
    def no_question(self):
        response = self.client.get(reverse("/"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list]",[]])

    def past_question(self):
        question = create_question(question_text = "Past question", days = -30)
        #object named question from Question model
        response = self.client.get(reverse("/"))
        self.assertQuerySetEqual(response.context["latest_question_list]",[question]])

#assertIs(a, b) This asserts that a is b — meaning that both refer to the exact same object in memory.

class QuestionDetailViewTests(TestCase):
     
     def future_question(self):
          fq=create_question(question_text="Future question", days = 5)
          url = reverse("detail", args = (fq.id))
          response = self.client.get(url)
          self.assertEqual(response.status_code, 404)

     def past_question(self):
          pq = create_question(question_text = "past question", days = -5)
          url = reverse("detail", args=(pq.id))
          response = self.client.get(url)
          self.assertContains(response, pq.question_text)