# Generated by Django 4.1.4 on 2023-03-02 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_lastpull'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adjectivechange',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='alimonychange',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='certificateofexcellence',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='demonstrator',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='dispatch',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='durationchange',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='extension',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='freeze',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='nomination',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='permissions',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='regularization',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='specializationchange',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='universitychange',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
        migrations.RenameField(
            model_name='universitydegree',
            old_name='date_modified',
            new_name='lastModifiedDate',
        ),
    ]