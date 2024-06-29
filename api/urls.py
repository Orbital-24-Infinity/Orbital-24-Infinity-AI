from django.urls import path
from api import views

urlpatterns = [
    path('', views.Quizzes),
    path('quizzes/', views.Quizzes),
    path('quizzes/<int:id>', views.QuizDetail),
    path('quizzes/questions/<int:id>', views.QuestionDetail)
]