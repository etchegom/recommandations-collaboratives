# Generated by Django 3.2.8 on 2021-10-18 09:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0027_taskfollowup"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskFollowupRsvp",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rsvp_followups",
                        to="projects.task",
                    ),
                ),
            ],
            options={
                "verbose_name": "rsvp suivi action",
                "verbose_name_plural": "rsvp suivis actions",
            },
        ),
    ]
