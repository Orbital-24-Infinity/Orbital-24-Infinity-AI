# Generated by Django 5.0.6 on 2024-07-24 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_id_user_userid_question_refdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='userid',
            field=models.ForeignKey(db_column='userID', default='', on_delete=django.db.models.deletion.DO_NOTHING, to='api.user'),
        ),
    ]
