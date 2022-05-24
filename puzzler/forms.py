from dataclasses import fields
from pyexpat import model
from django import forms
from . import models

class CreateAnswer(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = [ 'answer', 'solution']


class CreateQuestion(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['question_text', 'correct_answer']