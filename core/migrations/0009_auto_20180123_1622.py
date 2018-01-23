# Generated by Django 2.0 on 2018-01-23 16:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_flashcard_marked'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='history_back',
            field=models.CharField(default='', max_length=1200),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='last_trained_date_back',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last trained date back'),
        ),
    ]
