# Generated by Django 3.2.3 on 2021-10-26 14:19

from django.db import migrations, models
import django.db.models.deletion
import tagging.fields


class Migration(migrations.Migration):
    dependencies = [
        ("resources", "0016_auto_20210809_1230"),
        ("projects", "0029_project_exclude_stats"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskRecommandation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "condition",
                    tagging.fields.TagField(
                        blank=True, max_length=255, null=True, verbose_name="Condition"
                    ),
                ),
                ("text", models.TextField()),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resources.resource",
                    ),
                ),
            ],
        ),
    ]