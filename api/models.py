# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class File(models.Model):
    fileid = models.AutoField(primary_key=True)
    name = models.TextField()
    data = models.TextField(default="")
    topicid = models.ForeignKey('Topic', models.DO_NOTHING, db_column='topicID')  # Field name made lowercase.

    class Meta:
        db_table = 'File'


class Question(models.Model):
    questionid = models.AutoField(primary_key=True)
    question = models.TextField()
    mrq = models.BooleanField(default=False)
    openended = models.BooleanField(db_column='openEnded', default=False)  # Field name made lowercase.
    marked = models.BooleanField(default=False)
    selected = models.IntegerField(default=-1)
    topicid = models.ForeignKey('Topic', models.DO_NOTHING, db_column='topicID')  # Field name made lowercase.
    refdata = models.TextField(db_column='refData', default="")  # Field name made lowercase.

    class Meta:
        db_table = 'Question'


class Questionoptions(models.Model):
    questionoptionid = models.AutoField(primary_key=True)
    option = models.TextField()
    correct = models.BooleanField()
    questionid = models.ForeignKey(Question, models.DO_NOTHING, db_column='questionID')  # Field name made lowercase.

    class Meta:
        db_table = 'QuestionOptions'


class Topic(models.Model):
    topicid = models.AutoField(primary_key=True)
    title = models.TextField()
    maxquestions = models.IntegerField(db_column='maxQuestions', default=0)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', default=0)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='lastModified', auto_now=True)  # Field name made lowercase.
    isgenerating = models.BooleanField(db_column='isGenerating', default=False)  # Field name made lowercase.
    data = models.TextField()

    class Meta:
        db_table = 'Topic'


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    email = models.TextField(unique=True)
    lastlogin = models.DateTimeField(db_column='lastLogin', auto_now=True)  # Field name made lowercase.
    authkey = models.TextField(db_column='authKey')  # Field name made lowercase.
    authvalidity = models.DateTimeField(db_column='authValidity', auto_now=True)  # Field name made lowercase.

    class Meta:
        db_table = 'User'
