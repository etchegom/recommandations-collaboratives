# Generated by Django 3.2.3 on 2021-08-03 15:17

from django.db import migrations
import tagging.fields


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0008_auto_20210803_1554"),
    ]

    operations = [
        migrations.AddField(
            model_name="choice",
            name="signals",
            field=tagging.fields.TagField(blank=True, max_length=255),
        ),
    ]