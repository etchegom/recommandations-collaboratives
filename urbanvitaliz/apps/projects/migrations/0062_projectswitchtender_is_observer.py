# Generated by Django 3.2.15 on 2022-10-18 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0061_alter_project_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectswitchtender",
            name="is_observer",
            field=models.BooleanField(default=False),
        ),
    ]