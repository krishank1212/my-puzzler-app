
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Question, Answer, Subject, UserProfile, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import forms
from statistics import mode
from django.utils import timezone

def signup(request):
    if request.method == 'POST':
        user = request.POST['username']
        if User.objects.filter(username=user):
            return(redirect('/puzzler/signup?err_mesg=username'))
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return redirect('/puzzler/signup?err_mesg=pswd')
        elif len(password1) < 8:
            return redirect('/puzzler/signup?err_mesg=short')
        letters = re.search('[a-z]', password1)
        if not letters:
            return redirect('/puzzler/signup?err_mesg=lower')
        caps = re.search('[A-Z]', password1)
        if not caps:
            return redirect('/puzzler/signup?err_mesg=upper')
        nums = re.search('[0-9]', password1)
        if not nums:
            return redirect('/puzzler/signup?err_mesg=num')
        user = User.objects.create_user(user, password=password1)
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('/puzzler/')
    elif request.method == 'GET' :
        try:
            err_mesg = request.GET['err_mesg']
        except:
            return render (request, 'puzzler/signup.html')
        else:
            print(err_mesg)
            return render (request, 'puzzler/signup.html', {'err_mesg' : err_mesg})
        

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/puzzler/')
    else:
        form = AuthenticationForm()
    return render (request, 'puzzler/login.html', {'form' : form})

@login_required(login_url='/puzzler/login')
def logout_view(request):
    # if request.method == 'POST':
    
    logout(request)
 
    return redirect('/puzzler/login')
    # return render (request, 'puzzler/logout.html')

@login_required(login_url='/puzzler/login')
def subjects_view(request):
    subject_list = Subject.objects.order_by('subject_text')
    return render (request, 'puzzler/subjects.html', {'subject_list' : subject_list})



@login_required(login_url='/puzzler/login')
def question_post(request, subject_name):
    print('in question_view')
    print(request.POST['question_text'], request.POST['correct_answer'], request.user.username)
    question_text = request.POST['question_text']
    correct_answer = request.POST['correct_answer']
    form = forms.CreateQuestion({'question_text' : question_text, 'correct_answer' : correct_answer})
    subject = Subject.objects.get(subject_text=subject_name)
    if form.is_valid:
        print(request.user.username)
        instance  = form.save(commit=False)
        instance.user = request.user
        instance.subject = subject
        instance.pub_date = timezone.now()
        instance.save()
    form = forms.CreateQuestion()
    return redirect('subject_page', subject_name=subject_name)





def clean_answer(user_answer):
    user_answer = user_answer.lower().strip()
    user_words = user_answer.split()
    try:
        user_words.remove('the')
        user_words.remove('an')
        user_words.remove('a')
    except:
        pass
    print(f'{user_answer}: {user_words}')
    return user_words

def answer_correct(correct_answer, user_answer):
    user = clean_answer(user_answer)
    correct = clean_answer(correct_answer)
    return user == correct
    

@login_required(login_url='/puzzler/login')
def answer_view(request, subject_name, question_id):
    
    answer = request.POST['answer']
    user = request.user
    profile = UserProfile.objects.get(user=user.id)
    score = profile.score
    print(score)
    solution = request.POST['solution']
    form = forms.CreateAnswer({'answer':answer, 'solution':solution})
    question = Question.objects.get(id=question_id)
    question_user = UserProfile.objects.get(user=question.user)
    question_user.score += 1 
    print('Score:', question_user.user.username, question_user.score)
    if request.user == question.user:
        not form.is_valid 
    if form.is_valid:
        question.user_answers.add(request.user)
        print(request.user.username)
        instance = form.save(commit=False)
        instance.user = request.user
        instance.question = question
        instance.pub_date = timezone.now()
        if answer_correct(question.correct_answer, answer):
            print('User answer was correct')
            instance.correct = True
            profile.score += 2
            print(profile.score)
        else:
            instance.correct = False
            profile.score -= 1
            print(score)

        instance.save()
        profile.save()
        question_user.save()

        print(instance.answer)
        print(question.correct_answer.lower().strip())
         

    form = forms.CreateAnswer()
    print('Score at end of function: ', question_user.score)


    return redirect('question_page', subject_name=subject_name, question_id=question_id)   

@login_required(login_url='/puzzler/login')    
def subject_page(request, subject_name):
    subject = Subject.objects.get(subject_text=subject_name)
    questions = Question.objects.filter(subject=subject)
    form = forms.CreateQuestion()
    return render (request, 'puzzler/subjects_page.html', {'questions' : questions, 'subject' : subject, 'form' : form})

@login_required(login_url='/puzzler/login')
def question_page(request, question_id, subject_name):
    user = request.user
    user_id = user.id
    question = Question.objects.get(id=question_id)
    form = forms.CreateAnswer()
    empty = False
    if question.answer_set:
        empty = True
    return render (request, 'puzzler/question.html', {'question' : question, 'form' : form, 'subject_name' : subject_name, 'empty' : empty, 'user_id' : user_id} )

@login_required(login_url='/puzzler/login')
def user_page(request, user_id):
    user = User.objects.get(id=user_id)
    users = UserProfile.objects.order_by('-score')
    print(users)
    i = 0
    while users[i].user != user:
        print(i)
        i += 1
    rank = i + 1
    print(rank)
    score = UserProfile.objects.get(user=user).score
    print('Score: ', score)
    user_questions = Question.objects.filter(user=user)
    q_subjects = []
    for question in user_questions:
        q_subjects.append(question.subject)
        print(question)
        print(question.subject)
    print(q_subjects)
    user_answers = Answer.objects.filter(user=user)
    a_subjects = []
    for answer in user_answers:
        a_subjects.append(answer.question.subject)
    subjects = a_subjects + q_subjects
    try:
        fav_subj = mode(subjects)
    except:
        fav_subj = 'This user is idle and is yet to do anything on this AMAZING app!'
    else:
        print(fav_subj)
    return render (request, 'puzzler/user_page.html', {'score' : score, 'user': user, 'rank' : rank, 'fav_subj' : fav_subj})

@login_required(login_url='/puzzler/login')
def leaderboard(request):
    users = UserProfile.objects.order_by('-score')
    return render (request, 'puzzler/leaderboard.html', {'users' : users})
   
