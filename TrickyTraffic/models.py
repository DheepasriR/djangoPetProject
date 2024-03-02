from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


# Model to represent each question
class Question(models.Model):
    text = models.TextField()
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    correct_choice = models.CharField(max_length=200)


# Model to represent a quiz taken by a user
class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who took the quiz
    score = models.FloatField(default=0)  # Score achieved in the quiz
    quiz_taken_datetime = models.DateTimeField()  # Date and time when the quiz was taken

    def __str__(self):
        return f"{self.user.username}'s Quiz Result"


# Model to store user's answers to questions
class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # Quiz to which the answer belongs
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Question to which the answer belongs
    selected_choice = models.CharField(max_length=200)  # User's selected choice as an answer

    def __str__(self):
        return f"Answer for {self.question.text}"
