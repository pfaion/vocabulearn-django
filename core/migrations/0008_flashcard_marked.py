# Generated by Django 2.0 on 2018-01-18 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_flashcard_front_first'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='marked',
            field=models.BooleanField(default=False),
        ),
    ]