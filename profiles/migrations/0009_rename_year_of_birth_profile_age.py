# Generated by Django 3.2.22 on 2023-10-14 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_rename_birth_year_profile_year_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='year_of_birth',
            new_name='age',
        ),
    ]
