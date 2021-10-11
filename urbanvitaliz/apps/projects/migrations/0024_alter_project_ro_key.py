# Generated by Django 3.2.3 on 2021-10-04 12:14

from django.db import migrations, models
import urbanvitaliz.apps.projects.utils


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0023_alter_project_ro_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="ro_key",
            field=models.CharField(
                default=urbanvitaliz.apps.projects.utils.generate_ro_key,
                editable=False,
                max_length=32,
                unique=True,
                verbose_name="Clé d'accès lecture seule",
            ),
        ),
    ]