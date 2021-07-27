# Generated by Django 3.2.3 on 2021-07-20 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("addressbook", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="Courriel"
            ),
        ),
        migrations.AlterField(
            model_name="contact",
            name="first_name",
            field=models.CharField(blank=True, max_length=50, verbose_name="Prénom"),
        ),
        migrations.AlterField(
            model_name="contact",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="Nom de famille"
            ),
        ),
        migrations.AlterField(
            model_name="contact",
            name="phone_no",
            field=models.CharField(blank=True, max_length=20, verbose_name="Téléphone"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="name",
            field=models.CharField(max_length=90, verbose_name="Nom"),
        ),
    ]