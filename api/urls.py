from django.urls import path
from api import views

urlpatterns = [
    path('', views.Topics),
    path('quizzes/', views.Topics),
    path('quizzes/<int:id>', views.TopicDetail),
    path('quizzes/questions/<int:id>', views.QuestionDetail),
    path('quizzes/generate/<int:id>', views.Generate)
]