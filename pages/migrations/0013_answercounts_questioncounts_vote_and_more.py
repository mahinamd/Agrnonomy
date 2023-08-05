# Generated by Django 4.2.3 on 2023-07-31 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0012_answer_is_accepted'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('votes_count', models.IntegerField(default=0, verbose_name='Votes count')),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer_counts', to='pages.answer')),
            ],
            options={
                'verbose_name_plural': 'Answer Counts',
            },
        ),
        migrations.CreateModel(
            name='QuestionCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('votes_count', models.IntegerField(default=0, verbose_name='Votes count')),
                ('views_count', models.IntegerField(default=0, verbose_name='Views count')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='question_counts', to='pages.question')),
            ],
            options={
                'verbose_name_plural': 'Question Counts',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('upvote', models.BooleanField(default=False, verbose_name='Upvote')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('answer_vote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_votes', to='pages.answercounts', verbose_name='Answer Vote')),
                ('question_vote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_votes', to='pages.questioncounts', verbose_name='Question Vote')),
            ],
            options={
                'verbose_name_plural': 'Votes',
            },
        ),
        migrations.RemoveField(
            model_name='questioncount',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questioncount',
            name='voted_by',
        ),
        migrations.DeleteModel(
            name='AnswerCount',
        ),
        migrations.DeleteModel(
            name='QuestionCount',
        ),
        migrations.AddField(
            model_name='questioncounts',
            name='voted_by',
            field=models.ManyToManyField(blank=True, related_name='question_voted_content', through='pages.Vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answercounts',
            name='voted_by',
            field=models.ManyToManyField(blank=True, related_name='answer_voted_content', through='pages.Vote', to=settings.AUTH_USER_MODEL),
        ),
    ]