from django.db import models
from django.contrib.auth.models import User 

class Subject(models.Model):
    subject_text = models.CharField(max_length=17, primary_key=True, unique=True)
    
    def __str__(self):
        return self.subject_text

class Question(models.Model):
    question_text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')
    correct_answer = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user_answers = models.ManyToManyField(User, related_name='user_answers', default=None)
    
    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer = models.CharField(max_length=50)
    solution = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)




