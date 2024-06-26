from django.shortcuts import render
from rest_framework import generics
from .serializers import QuizSerializer
from .models import Quiz

# Create your views here.


class QuizView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class= QuizSerializer