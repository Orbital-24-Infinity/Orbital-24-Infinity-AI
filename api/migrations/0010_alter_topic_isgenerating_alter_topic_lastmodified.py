# Generated by Django 5.0.6 on 2024-07-01 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_delete_authgroup_delete_authgrouppermissions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='isgenerating',
            field=models.BooleanField(db_column='isGenerating', default=False),
        ),
        migrations.AlterField(
            model_name='topic',
            name='lastmodified',
            field=models.DateTimeField(auto_now=True, db_column='lastModified'),
        ),
    ]
