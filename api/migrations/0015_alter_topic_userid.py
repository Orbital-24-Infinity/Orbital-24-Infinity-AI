# Generated by Django 5.0.6 on 2024-07-24 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_topic_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='userid',
            field=models.ForeignKey(db_column='userID', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='api.user'),
        ),
    ]
