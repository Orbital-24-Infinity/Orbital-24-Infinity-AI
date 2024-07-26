from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from .serializers import TopicSerializer, QuestionSerializer, QuestionGenSerializer
from .models import Topic, Question, Questionoptions, File
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import random

# Create your views here.

@api_view(['GET', 'POST'])
def Topics(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return JsonResponse({'topics': serializer.data})

    elif request.method == 'POST':
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            topic = serializer.save()

            passage = topic.data
            generatedQuestions = GenerateQuestions(passage)

            for questionText, options in generatedQuestions.items():
                question = Question.objects.create(
                    question=questionText[0],
                    refdata=questionText[1],
                    topicid=topic
                )

                for optionText, check in options.items():
                    Questionoptions.objects.create(
                        option=optionText,
                        correct=check,
                        questionid=question
                    )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def TopicDetail(request, id):
    
    try:
        topic = Topic.objects.get(pk=id)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicSerializer(topic)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def QuestionDetail(request, id):
    if request.method == 'GET':
        try:
            quiz = Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuestionSerializer(quiz)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def Generate(request, id):
    if request.method == 'POST':
        try:
            topic = Topic.objects.get(pk=id)
        except Topic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuestionGenSerializer(topic, data=request.data)
        if serializer.is_valid():
            topic = serializer.save()

            topic.isgenerating = True

            passage = topic.data
            files = File.objects.filter(topicid=topic)
            for file in files:
                passage += file.data
            generatedQuestions = GenerateMore(passage)

            for questionText, options in generatedQuestions.items():
                question = Question.objects.create(
                    question=questionText[0],
                    refdata=questionText[1],
                    topicid=topic
                )

                for optionText, check in options.items():
                    Questionoptions.objects.create(
                        option=optionText,
                        correct=check,
                        questionid=question
                    )
            
            topic.maxquestions += 10
            topic.isgenerating = False
            topic.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#functions for generating questions

def RunInference(passage, tokenizer, model, device):
    input_text = f"passage: {passage}"
    input_enc = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding='max_length')
    input_ids = input_enc.input_ids.to(device)
    attention_mask = input_enc.attention_mask.to(device)
    
    outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=512)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_text

def GenerateQuestions(passage):
    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    model = T5ForConditionalGeneration.from_pretrained("t5-large")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    #generate the questions first
    model.load_state_dict(torch.load("model_state.pt"))
    model.to(device)
    model.eval()

    length = len(passage)
    start, end = 0, 0
    questions = []
    fullstops = 0
    for i in range(length // 2):
        if passage[i] == ".":
            fullstops += 1
            
    if fullstops > 3:
        for i in range(10):
            end = int((i + 1) / 10 * length)
            while end < length and passage[end] != ".":
                end += 1
            if end < length and passage[end] == ".":
                end += 1
            question = RunInference(passage[start:end], tokenizer, model, device)
            questions.append((question, passage[start : end]))
            start = end
    else:
        for i in range(10):
            end = int((i + 1) / 10 * length)
            question = RunInference(passage[start:end], tokenizer, model, device)
            questions.append((question, passage[start : end]))
            start = end
    
    #then we generate the options and answers for the question
    model.load_state_dict(torch.load("options_model_state.pt"))
    model.to(device)
    model.eval()

    start, end = 0, 0
    output = {}

    for i in range(10):
        start = end
        end = int((i + 1) / 10 * length)
        if questions[i] == "repeat question":
            continue
        optionsPrompt = f"passage: {passage[start:end]} question: {question[i]}"
        options = RunInference(optionsPrompt, tokenizer, model, device)

        optionsDic = {}
        startOfOption = 0
        currentOption = 0
        correctOption = ord(options[-1]) - 65
        for optionsIndex in range(len(options)):
            if options[optionsIndex] == '&' or options[optionsIndex] == '#':
                option = options[startOfOption:optionsIndex]
                optionsDic[option] = currentOption == correctOption
                currentOption += 1
                startOfOption = optionsIndex + 1
                
        output[questions[i]] = optionsDic

    return output


def GenerateMore(passage):
    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    model = T5ForConditionalGeneration.from_pretrained("t5-large")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    #generate the questions first
    model.load_state_dict(torch.load("model_state.pt"))
    model.to(device)
    model.eval()

    length = len(passage)
    start, end = 0, 0
    questions = []

    fullstops = 0
    for i in range(length // 2):
        if passage[i] == ".":
            fullstops += 1

    if fullstops > 3:
        while len(questions) < 10:
            mid = random.randint(0, length - 1)
            start, end = mid, mid

            while start > 0 and passage[start] != ".":
                start -= 1
            if start != 0:
                start += 2
            while end < length and passage[end] != ".":
                end += 1
            if end < length and passage[end] != ".":
                end += 1
            end += 1
            
            question = RunInference(passage[start:end], tokenizer, model, device)
            if not any(q[0] == question for q in questions):
                questions.append((question, passage[start : end]))
    else:
        while len(questions) < 10:
            start = random.randint(0, length - 1)
            end = start
            while end < length and end - start < length // 5:
                end += 1

            question = RunInference(passage[start:end], tokenizer, model, device)
            if not any(q[0] == question for q in questions):
                questions.append((question, passage[start:end]))
                
    model.load_state_dict(torch.load("options_model_state.pt"))
    model.to(device)
    model.eval()

    output = {}

    for question in questions:
        optionsPrompt = f"passage: {question[1]} question: {question[0]}"
        options = RunInference(optionsPrompt, tokenizer, model, device)

        optionsDic = {}
        startOfOption = 0
        currentOption = 0
        correctOption = ord(options[-1]) - 65
        for optionsIndex in range(len(options)):
            if options[optionsIndex] == '&' or options[optionsIndex] == '#':
                option = options[startOfOption:optionsIndex]
                optionsDic[option] = currentOption == correctOption
                currentOption += 1
                startOfOption = optionsIndex + 1
                
        output[question] = optionsDic

    return output
