# Generated by Django 4.2.3 on 2023-07-19 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managements', '0002_rename_bn_value_1_information_bn_details_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='information',
            old_name='bn_details',
            new_name='details_bn',
        ),
        migrations.RenameField(
            model_name='information',
            old_name='en_details',
            new_name='details_en',
        ),
        migrations.RenameField(
            model_name='information',
            old_name='bn_name',
            new_name='name_bn',
        ),
        migrations.RenameField(
            model_name='information',
            old_name='en_name',
            new_name='name_en',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='information',
        ),
        migrations.AddField(
            model_name='information',
            name='subcategory',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='managements.subcategory'),
            preserve_default=False,
        ),
    ]