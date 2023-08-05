# Generated by Django 4.2.3 on 2023-08-04 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='rme',
            new_name='expert',
        ),
        migrations.RemoveField(
            model_name='account',
            name='address_line',
        ),
        migrations.RemoveField(
            model_name='account',
            name='city',
        ),
        migrations.RemoveField(
            model_name='account',
            name='country',
        ),
        migrations.RemoveField(
            model_name='account',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='account',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='account',
            name='house_no',
        ),
        migrations.RemoveField(
            model_name='account',
            name='social_fb',
        ),
        migrations.RemoveField(
            model_name='account',
            name='social_li',
        ),
        migrations.RemoveField(
            model_name='account',
            name='social_tw',
        ),
        migrations.RemoveField(
            model_name='account',
            name='zip_code',
        ),
    ]