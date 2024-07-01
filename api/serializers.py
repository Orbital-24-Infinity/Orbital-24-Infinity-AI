from rest_framework import serializers
from .models import File, Question, Questionoptions, Topic


class QuestionoptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionoptions
        fields = ('questionoptionid', 'option', 'correct', 'questionid')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('fileid', 'name' , 'path', 'topicid')

class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionoptionsSerializer(many=True, read_only=True, source='questionoptions_set')

    class Meta:
        model = Question
        fields = ('questionid', 'question', 'mrq', 'openended', 'marked', 'selected', 'topicid', 'options')


class TopicSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')
    files = FileSerializer(many=True, read_only=True, source='file_set')
    
    class Meta:
        model = Topic
        fields = ('topicid', 'title', 'maxquestions', 'userid', 'lastmodified', 'isgenerating', 'data', 'questions', 'files')


class QuestionGenSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')
    files = FileSerializer(many=True, read_only=True, source='file_set')
    
    class Meta:
        model = Topic
        fields = ('topicid', 'isgenerating', 'lastmodified', 'questions', 'files')