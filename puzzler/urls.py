from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('', views.subjects_view, name='subjects'),
    path('leaderboard', views.leaderboard, name='leaderboard'),


    path('subject/<str:subject_name>/', views.subject_page, name='subject_page'),
    path('subject/<str:subject_name>/question', views.question_post, name='question_post'),
    path('user/<int:user_id>', views.user_page, name='user_page'),

    path('subject/<str:subject_name>/<int:question_id>/', views.question_page, name='question_page'),    
    path('subject/<str:subject_name>/<int:question_id>/answer', views.answer_view, name='answer'),

]
