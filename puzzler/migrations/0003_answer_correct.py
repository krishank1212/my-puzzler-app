# Generated by Django 3.2.7 on 2022-03-18 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzler', '0002_rename_answer_text_answer_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False),
        ),
    ]
