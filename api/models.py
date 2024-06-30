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
    path = models.TextField(unique=True)
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
    maxquestions = models.IntegerField(db_column='maxQuestions')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='lastModified')  # Field name made lowercase.
    isgenerating = models.BooleanField(db_column='isGenerating')  # Field name made lowercase.
    data = models.TextField()

    class Meta:
        db_table = 'Topic'


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    email = models.TextField(unique=True)
    lastlogin = models.DateTimeField(db_column='lastLogin')  # Field name made lowercase.
    authkey = models.TextField(db_column='authKey')  # Field name made lowercase.
    authvalidity = models.DateTimeField(db_column='authValidity')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
