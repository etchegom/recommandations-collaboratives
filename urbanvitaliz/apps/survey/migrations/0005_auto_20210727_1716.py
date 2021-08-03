# Generated by Django 3.2.3 on 2021-07-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0004_session_survey"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="comment",
            field=models.TextField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name="answer",
            unique_together={("session", "question")},
        ),
    ]