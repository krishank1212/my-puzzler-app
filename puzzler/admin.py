from re import A
from django.contrib import admin

from .models import Subject, Question, Answer, UserProfile

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProfile)

# Register your models here.
